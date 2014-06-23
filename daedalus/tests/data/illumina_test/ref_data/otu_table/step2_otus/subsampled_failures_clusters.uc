# uclust --maxrejects 500 --input /tmp/UclustExactMatchFilter4TzArr2SvlGg1ASF5M9d.fasta --id 0.97 --tmpdir /tmp --w 12 --stepwords 20 --usersort --maxaccepts 20 --stable_sort --uc otu_table//step2_otus/subsampled_failures_clusters.uc
# version=1.2.22
# Tab-separated fields:
# 1=Type, 2=ClusterNr, 3=SeqLength or ClusterSize, 4=PctId, 5=Strand, 6=QueryStart, 7=SeedStart, 8=Alignment, 9=QueryLabel, 10=TargetLabel
# Record types (field 1): L=LibSeed, S=NewSeed, H=Hit, R=Reject, D=LibCluster, C=NewCluster, N=NoHit
# For C and D types, PctId is average id with seed.
# QueryStart and SeedStart are zero-based relative to start of sequence.
# If minus strand, SeedStart is relative to reverse-complemented seed.
S	0	137	*	*	*	*	*	QiimeExactMatch.L1S287_21070	*
S	1	133	*	*	*	*	*	QiimeExactMatch.L2S232_38470	*
C	0	1	*	*	*	*	*	QiimeExactMatch.L1S287_21070	*
C	1	1	*	*	*	*	*	QiimeExactMatch.L2S232_38470	*
