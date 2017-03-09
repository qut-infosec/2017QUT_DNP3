_DATA_SET=$(echo `pwd | cut -d "/" -f10`)
_ATTACK=$(echo `pwd | cut -d "/" -f7`)
_DATA_TYPE=$(echo `pwd | cut -d "/" -f9`)
_TITLE=$(echo $_DATA_SET $_ATTACK":" $_DATA_TYPE "Set" | awk '{for (i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
echo $_TITLE
gnuplot -e "_TITLE='${_TITLE}'" gnuplot_graphs.gplot