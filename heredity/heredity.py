import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    for person in people:
        # We assume assume that either mother and father are both blank
        # (no parental information in the data set),
        # or mother and father will both refer to other people
        # in the people dictionary
        if people[person]["mother"] or people[person]["father"]:
            mother = {"name": people[person]["mother"]}
            father = {"name": people[person]["father"]}

            if mother["name"] in one_gene:
                mother["num_genes"] = 1
            elif mother["name"] in two_genes:
                mother["num_genes"] = 2
            else:
                mother["num_genes"] = 0

            if father["name"] in one_gene:
                father["num_genes"] = 1
            elif father["name"] in two_genes:
                father["num_genes"] = 2
            else:
                father["num_genes"] = 0

        else:
            mother = {"name": None}
            father = {"name": None}

        if person in one_gene:
            probability *= one_gene_probability(person, mother, father)
            num_genes = 1
        elif person in two_genes:
            probability *= two_genes_probability(person, mother, father)
            num_genes = 2
        else:
            probability *= no_genes_probability(person, mother, father)
            num_genes = 0

        if person in have_trait:
            probability *= PROBS["trait"][num_genes][True]
        else:
            probability *= PROBS["trait"][num_genes][False]

    return probability


def from_parents_probability(person, mother, father):
    """
    Calculate the probability that person got a gene
    from his mother and another probability, that person
    got a gene from his father
    "mother" and father are dicts with the following structure
    mother = {"name": name, "num_genes": num_genes}
    father = {"name": name, "num_genes": num_genes}
    """
    if mother["num_genes"] == 0:
        # If mother has no genes, the only way
        # 'person' got a gene from her is through mutation
        from_mother_prob = PROBS["mutation"]
    elif mother["num_genes"] == 1:
        # If mother has 1 gene, 'person' got it
        # with probability 0.5 and it did not go through mutation,
        # with probability PROBS["mutation"]
        # or did not get the gene, but it went through mutation
        from_mother_prob = (0.5*negation(PROBS["mutation"]) +
                            0.5*PROBS["mutation"])
        # The expression above is always equals to 0.5,
        # but the long expression was used for the sake of clarity
    else:
        # Mother has 2 genes
        from_mother_prob = 1 - PROBS["mutation"]

    if father["num_genes"] == 0:
        from_father_prob = PROBS["mutation"]
    elif father["num_genes"] == 1:
        from_father_prob = (0.5*negation(PROBS["mutation"]) +
                            0.5*PROBS["mutation"])
    else:
        from_father_prob = 1 - PROBS["mutation"]

    return from_mother_prob, from_father_prob


def negation(probability):
    """
    Returns the negation of the probability,
    e.g. negation(from_mother_prob) returns the probability
    that person DID NOT get a gene from his mother
    """
    return 1 - probability


def no_genes_probability(person, mother, father):
    """
    Calculate the probability that person has no genes.
    "mother" and father are dicts with the following structure
    mother = {"name": name, "num_genes": num_genes}
    father = {"name": name, "num_genes": num_genes}
    If there are no available information on the parents,
    "name" should be None
    """
    # It is assumed that either mother and father are both unknown,
    # or are both known
    if mother["name"] is None or father["name"] is None:
        # No information about the parents is available
        # Unconditional probability is used in this case
        return PROBS["gene"][0]

    else:
        # Information about the parents is available.
        # 'person' must not get the gene from his mother and from his father
        from_mother_prob, from_father_prob = from_parents_probability(person, mother, father)

        probability = negation(from_father_prob)*negation(from_mother_prob)

        return probability


def one_gene_probability(person, mother, father):
    """
    Calculate the probability that person has one gene.
    "mother" and father are dicts with the following structure
    mother = {"name": name, "num_genes": num_genes}
    father = {"name": name, "num_genes": num_genes}
    If there are no available information on the parents,
    "name" should be None
    """
    # It is assumed that either mother and father are both unknown,
    # or are both known
    if mother["name"] is None or father["name"] is None:
        # No information about the parents is available
        # Unconditional probability is used in this case
        return PROBS["gene"][1]

    else:
        # Information about the parents is available.
        # Either 'person' gets the gene from his mother and not his father,
        # or he gets the gene from his father and not his mother
        from_mother_prob, from_father_prob = from_parents_probability(person, mother, father)

        probability = (from_mother_prob*negation(from_father_prob) +
                       from_father_prob*negation(from_mother_prob))

        return probability


def two_genes_probability(person, mother, father):
    """
    Calculate the probability that person has two genes.
    "mother" and father are dicts with the following structure
    mother = {"name": name, "num_genes": num_genes}
    father = {"name": name, "num_genes": num_genes}
    If there are no available information on the parents,
    "name" should be None
    """
    # It is assumed that either mother and father are both unknown,
    # or are both known
    if mother["name"] is None or father["name"] is None:
        # No information about the parents is available
        # Unconditional probability is used in this case
        return PROBS["gene"][2]

    else:
        # Information about the parents is available.
        # 'person' must get one gene from his mother and
        # one from his father
        from_mother_prob, from_father_prob = from_parents_probability(person, mother, father)

        probability = (from_mother_prob*from_father_prob)

        return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        else:
            num_genes = 0

        probabilities[person]["gene"][num_genes] += p

        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait_sum = sum(probabilities[person]["trait"].values())
        gene_sum = sum(probabilities[person]["gene"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = (probabilities[person]["trait"][trait] /
                                                     trait_sum)

        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = (probabilities[person]["gene"][gene] /
                                                   gene_sum)


if __name__ == "__main__":
    main()
