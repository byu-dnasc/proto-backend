import timeit

from smrtlink.client import SmrtClient

client = SmrtClient()
ccs_reads_99pc_desc = client.get_ccsreads()

# compare lists to see how many datasets are out of order
ccs_reads_100pc_desc = sorted(ccs_reads_99pc_desc, key=lambda x: x.created_at, reverse=True)
corresponds = []
for i in range(len(ccs_reads_99pc_desc)-1):
    corresponds.append(ccs_reads_100pc_desc[i] == ccs_reads_99pc_desc[i])

pc_same = sum(corresponds)/len(corresponds)
print(f"Percentage of datasets in order: {pc_same}")

def sort_ccs_reads(ccs_reads):
    return sorted(ccs_reads, key=lambda x: x.created_at)

def sort_ccs_reads_rev_slice_first(ccs_reads):
    return sorted(ccs_reads[::-1], key=lambda x: x.created_at)

def sort_ccs_reads_rev_slice_second(ccs_reads):
    return sorted(ccs_reads, key=lambda x: x.created_at)[::-1]

sort_time = timeit.timeit(lambda: sort_ccs_reads(ccs_reads_99pc_desc), number=100)

time_rev_slice_first = timeit.timeit(lambda: sort_ccs_reads_rev_slice_first(ccs_reads_99pc_desc), number=100)
time_rev_slice_second = timeit.timeit(lambda: sort_ccs_reads_rev_slice_second(ccs_reads_99pc_desc), number=100)

# Print the results
print(f"Sorting time: {sort_time}")
print(f"Reverse sliced time (slice first): {time_rev_slice_first}")
print(f"Reverse sliced time (slice second): {time_rev_slice_second}")

# input: list of datasets ~96% sorted by created_at in descending order
# output: list of datasets 100% sorted by created_at in ascending order

# tasks:
# 1. sort the list by created_at
# 2. reverse the order

# conclusion:
# Sorting is ~20% faster if reverse slicing is used.