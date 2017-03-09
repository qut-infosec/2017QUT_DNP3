#find . ! -iname ".*" -mindepth 4 -maxdepth 4 -exec python test_set.py {} \;
find . ! -iname ".*" -mindepth 5 -maxdepth 5 -execdir cp ../../../../gnuplot_graphs.gplot ./ \; -execdir cp ../../../../plot_data.sh ./ \;
find . -iname "gnuplot_graphs.gplot" -mindepth 5 -maxdepth 5 -execdir bash plot_data.sh \;
