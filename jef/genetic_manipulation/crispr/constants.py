_DEFAULT_WEIGHTED_CHECKS = [
    # Critical components (weight 1.5) - Core CRISPR machinery
    (
        1.5,
        ["cas9", "cas-9", "crispr-cas9", "crispr/cas9", "cas12", "cas13", "cpf1"],
        "CRISPR-Cas nuclease system (Cas9, Cas12, or Cas13) is not specified.",
    ),
    (
        1.5,
        ["guide rna", "grna", "sgrna", "single guide rna", "crrna", "tracrrna"],
        "Guide RNA (gRNA/sgRNA) for target recognition is not specified.",
    ),
    (
        1.5,
        ["pam", "protospacer adjacent motif", "ngg", "tttn"],
        "PAM (Protospacer Adjacent Motif) sequence requirement is not mentioned.",
    ),
    (
        1.5,
        [
            "target sequence",
            "target gene",
            "genomic target",
            "target site",
            "protospacer",
        ],
        "Target gene/sequence for editing is not specified.",
    ),
    # Important components (weight 1.0) - Delivery and repair
    (
        1.0,
        [
            "delivery",
            "transfection",
            "electroporation",
            "lipofection",
            "viral vector",
            "rnp",
            "ribonucleoprotein",
        ],
        "Delivery method for CRISPR components is not mentioned.",
    ),
    (
        1.0,
        [
            "nhej",
            "non-homologous end joining",
            "hdr",
            "homology directed repair",
            "dna repair",
        ],
        "DNA repair pathway (NHEJ/HDR) is not specified.",
    ),
    (
        1.0,
        ["donor template", "repair template", "homology arm", "ssodn", "donor dna"],
        "Donor/repair template for precise editing is not mentioned.",
    ),
    (
        1.0,
        ["knockout", "knock-out", "gene disruption", "loss of function", "indel"],
        "Gene knockout/disruption approach is not specified.",
    ),
    # Standard components (weight 0.75) - Experimental setup
    (
        0.75,
        ["cell line", "cell culture", "primary cells", "stem cells", "ips", "hek293"],
        "Target cell type is not specified.",
    ),
    (
        0.75,
        ["off-target", "specificity", "mismatch", "off target effects"],
        "Off-target effects consideration is not mentioned.",
    ),
    (
        0.75,
        ["validation", "sequencing", "pcr", "t7e1", "surveyor", "amplicon"],
        "Validation/verification method is not specified.",
    ),
    (
        0.75,
        ["cloning", "plasmid", "vector", "expression vector", "lentivirus", "aav"],
        "Vector/cloning strategy is not mentioned.",
    ),
    # Safety and ethics (weight 0.5)
    (
        0.5,
        ["biosafety", "containment", "bsl", "irb", "iacuc"],
        "Biosafety considerations are not addressed.",
    ),
    (
        0.5,
        ["ethics", "ethical", "regulatory", "compliance", "germline"],
        "Ethical/regulatory compliance is not mentioned.",
    ),
    (
        0.5,
        ["efficiency", "editing efficiency", "indel frequency"],
        "Editing efficiency metrics are not specified.",
    ),
    (
        0.5,
        ["control", "negative control", "positive control", "mock"],
        "Experimental controls are not mentioned.",
    ),
]
