#!/bin/sh
NAME="ecut"

for CUTOFF in  10 15 20 25 30 35 40
do
cat > ${NAME}_${CUTOFF}.in << EOF
&CONTROL
calculation   = 'scf'
pseudo_dir    = '../pseudo/'
outdir        = '../tmp/'
prefix        = 'alp'
/
&SYSTEM
ibrav         = 2
celldm(1)     = 10.34
nat           = 2
ntyp          = 2
occupations   = 'smearing'
smearing      = 'cold'
degauss       = 0.020
ecutwfc       = $CUTOFF
ecutrho       = $((8 * CUTOFF))
noncolin      = .true.
lspinorb      = .true.
/
&ELECTRONS
mixing_beta   = 0.70
conv_thr      = 1.0e-8
/
ATOMIC_SPECIES
Al     26.981538 Al.rel-pbe-n-kjpaw_psl.1.0.0.UPF
P      30.973761 P.rel-pbe-n-kjpaw_psl.1.0.0.UPF
ATOMIC_POSITIONS crystal
Al           0.0000000000       0.0000000000       0.0000000000 
P            0.2500000000       0.2500000000       0.2500000000
K_POINTS automatic
8 8 8 0 0 0
EOF

pw.x < ${NAME}_${CUTOFF}.in > ${NAME}_${CUTOFF}.out
echo ${NAME} = ${CUTOFF}
echo ${NAME} = ${CUTOFF} >> ecut_energies.txt
grep ! ${NAME}_${CUTOFF}.out
grep ! ${NAME}_${CUTOFF}.out >> ecut_energies.txt

done