rm -r res traces
mv output_run.txt old_output_run.txt
qsub run.pbs
qstat
