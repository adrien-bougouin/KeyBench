#!/usr/bin/perl

# Marie Candito

# DEBUGS TODO : mm.   km/h 
use Getopt::Long;
$help = 0 ;
$nomissingspaces = 0 ;
$nodashsep = 0 ;
$outsep='space' ;
GetOptions("outsep:s" =>\$outsep,
	   "nomissingspaces!" => \$nomissingspaces,
	   "nodashsep!" => \$nodashsep,
           "help!" => \$help) or die (&usage) ;

die(&usage) unless (!$help and ($outsep eq 'newline' or $outsep eq 'space')) ;

sub usage
{
    return "Tokenizer for French raw text.
Usual ponctuation used as separator.
Hyphen *is not* a separator, except for a list of tokens ending with -
Period *is* considered a separator, when followed by a space char, and except a list of tokens ending with . Also in cases like two alphabetic tokens separated by a period, with the second token starting with a capital letter (example : 'la vie.Et aussi la mort'). To disable this case, use -nomissingspaces option.

$0 
[-outsep [newline|space]] : separator for tokens in output (default=space)] 
[-nomissingspaces] : if set, won't consider a period as separator if not followed by a space. Default : set 
[ -help ]\n" ;
}
# -------------------------------------
# data
# plain separators
@separators = ('...','..','(',')','[',']','{','}','!',';','?','"','<','>','«','»',' ','&','§','$','%','#') ;
# '.' is a separator only when followed by \s or \t , or end of line
# hence "56.78.89" "deallu.com" won't be separated.  (pb for missing spaces)
# "," is a separator only if
# -- not followed by a digit (34,aussi)
# -- followed by a digit but not preceded by a digit (trois,3)
# ":" is a separator only if not followed by //
# "/" is a separator only if not preceded by : or /, and not preceded by a digit or not followed by a digit
# so '/' is a separator in "7 jours/7" or "assureurs/assurés" or "m3/heure" but not in "1/10e"
# ' is a separator except in cases like "Jean-l'Hôte"
@re_separators = ('\.(?=[\s\t])', '\.$',',(?![0-9])','(?<![0-9]),(?=[0-9])',':(?!//)', '(?<![:\/0-9])/','(?<![:\/])/(?![0-9])', "(?<![a-zéêèïîôöûüùàâ]\-l)'") ;

$url_http_or_ftp = '(?:^|(?<=\s))(?:Http|HTTP|http|FTP|ftp)[sS]?:\/\/[a-zA-Z0-9\_\-]+(?:\.[a-zA-Z0-9_\-]+)*(?:\:[0-9]+)?(?:\/[a-zA-Z0-9\_\-~\?\%\=\&\#]+(?:\.[a-zA-Z0-9\_\-\?\%\=\&\#]+)*)*\/?' ;

# at least three members xxx.xxx.xxx + at least one /xxx
# (cf. fff.fff.fff are handled already)
$other_potential_urls = '(?:^|(?<=\s))[a-zA-Z]+\.[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+(?:\/[a-zA-Z0-9\_\-]+(?:\.[a-zA-Z0-9\_\-]+)*)+' ;

$other_with_slash = '(?:^|(?<=\s))[0-9]+(?:\/[0-9]+[a-zA-Z0-9]*)+' ;

# known tokens ending with quote
@EndingWithQuote = ('c','m','n','j','s','t','aujourd','d','l','qu','puisqu','lorsqu','quelqu','presqu','prud','quoiqu','jusqu') ;

# known tokens ending with dots
@EndingWithDot = ('tel','tél','etc','e.g','ex','num','p','pp','fig','m','i.e','c.a.d','c.à.d') ;

# --------------------------------------
# Build variables with these data

$outsepchar = ($outsep eq 'newline') ? "\n" : " " ; 

# build a regexp with these separators
@separators =  map { s/(.)/\\$1/g ; $_ ; } @separators ;
@separators = (@separators, @re_separators, $url_http_or_ftp, $other_potential_urls) ;
$re_separator = join('|', @separators) ;

%hEndingWithQuote = () ;
map { $hEndingWithQuote{$_} = 1 ; } @EndingWithQuote ;
%hEndingWithDot = () ;
map { $hEndingWithDot{$_} = 1 ; } @EndingWithDot ;

# -------------------------------------
while(<>) 
{
    chomp ;
    s/ / /g ;
    s/[\t ]+/ /g ;
    # space normalisation
    s/^\s*// ;
    s///g ; 
    # skip empty lines
    next unless ($_) ;

    # .- should be split, if followed by space
    s/\.- /\. -/g ;
    # ** If first token is 'A', then it is very very likely to mean 'à'
    #    (this is needed very soon, before any further change, e.g. 'A-t-il' should not match, 'A.' should not match...)
    s/(^|[\.\?\!;]\s)([\'\"\«\-]\s?)?A(\s)/$1$2à$3/go ;
    # ** hyphenated suffixes
    #    donnez-le-nous => donnez -le -nous
    s/-(l(?:es?|a|eur|ui)|y|[vn]ous|[mt](?:\'|oi))-(l(?:es?|a|eur)|y|en|[vn]ous|[mt]oi)(?![\wéèêîôûëïüäù\-])/ -$1 -$2/go ;
    #    doit-elle => doit -elle
    #    ira-t-elle => ira -t-elle
    #    ira - t -elle => ira => -t-elle
    # (but not : arc-en-ciel =/=> arc -en-ciel
    #            Paulez-luigi =/=> Paulez -luigi ...)
    s/(- ?t ?)?-(ce|elles?|ils?|en|on|je|la|les?|leur|lui|[mt]oi|nous|tu|y)(?![\wéèêîôûëïüäù\-])/ $1-$2/go ;
    # special handling of post-verbal clitic -vous : do separate, except if 'rendez-vous' ...
    s/(?<!rendez)-(vous)(?![\wéèêîôûëïüäù])/ -$1/goi ;

    # donne-m'en => donne -m'en
    s/(- ?t ?)?-([mlt]\'(?:en|y))/ $1-$2/go ;

    # ** hyphenated prefixes
    #    anti-bush => anti- bush
    #    franco-canadien => franco- canadien
    s/((?:o|(?:^|\s|\')(?:anti|non|bi))-)/$1 /igo ;

    # ** unless otherwise specified, a period is a separator between two alphabetical tokens, if the second starts with a capital letter
    unless ($nomissingspaces)
    {
	s/((?:^|\s)[A-Z]?[a-zéèêçîôûâùìòà\-]+(?: *(?:\'|»|«))?\.)([A-Z])/$1 $2/go ;
    }
    
    @line = split(/ *($re_separator) */) ;
    # ** if line starts with a separator, then line[0] is '', => get rid of it
    while ($line[0] eq '' or $line[0] eq ' ') { shift(@line); }
    print $line[0] ;
    $rk = 1 ;
    while ($rk <= $#line)
    { 
	$t = $line[$rk] ;
#	print "\nT=$t\n";
	if ($t eq ' ' or $t eq '') 
	{
	    $rk++ ;
	    next ;
	}
	$sep = 1 ;
	$previous = lc($line[$rk -1]) ;
	if ($t eq "'")
	{
	    $sep = 0 if ($hEndingWithQuote{ $previous }) ;
	}
	elsif ($t eq '.')
	{
	    $sep = 0 if ($hEndingWithDot{ $previous } or $previous =~ /^[a-z](?:\.[a-z])+$/o) ;
	}

	print $outsepchar if ($sep) ;
	# tokens ending with -, or beginning with -, e.g. :
	# "bla bla bla -bli bli bli- bla bla bla"
	unless ($nodashsep)
	{   
	    # ending with -
	    if ($t =~ /^(.+)\-$/) # separate, unless anti- non- ...o- bi-
	    {
		$pref = $1 ;
		$t = $pref.$outsepchar.'-' unless (lc($pref) =~ /^(anti|bi|non)$|o$/) ;
	    }
	    # beginning with -
	    if (($t !~ /(- ?t ?)?-(ce|elles?|ils?|en|on|je|la|les?|leur|lui|[mt]oi|[nv]ous|tu|y)$/) and ($t =~ /^\-([^0-9].*)/))
	    {
		$t = '-'.$outsepchar.$1 ;
	    }
	}
	print $t ;
	$rk ++ ;
    }
    print "\n" ;
}



    
