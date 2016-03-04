use strict;
use warnings;

my %words;
my $long_count = 0;
my $total = 0;
while(<>) {
    s/[\'\"\.\-\!\?\,\:\;\)\(\[\]]/ /g; # remove punctuation
    $_ = lc $_;
#    print;
    my @w = split(/\s+/,$_);
    for my $w ( @w ) {
	$total++;
	$long_count++ if( length($w) > 5 ) ;
	$words{$w}++;
    }
}

my $i = 1;
for my $n ( sort { $words{$b} <=> $words{$a} } keys %words ) {
    print join("\t", $i++, $n, $words{$n}, 
	       sprintf("%.2f%%",100 * $words{$n} / $total)), 
	       "\n";
}

print "===\n";
$i = 1;
for my $n ( sort { $words{$b} <=> $words{$a} } keys %words ) {
    next if length($n) < 5;
    print join("\t", $n, $words{$n}, 
	       sprintf("%.2f%%",100 * $words{$n} / $long_count), length($n)),
	       "\n";
}

