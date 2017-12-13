#!/usr/bin/perl -w

use strict;
use warnings;
use File::Find;
use File::Basename;
use File::Slurp;
use List::MoreUtils qw(uniq);

# Set location of html files (and others)
my $file_directory = "/usr/local/apache2/htdocs/";
my $stop_file = "/usr/local/bin/stopwords.txt";
my $out_file = "/usr/local/bin/html_index.txt";

# Get list of files, with their full filepath
my @files;
find( \&wanted, $file_directory);

# Get list of stop words
my @stop_words = read_file($stop_file, chomp => 1);

# Open output file for writing
open(my $writer, '>', $out_file) or die "Could not open file $out_file $!";

# Iterate through each file
foreach my $file (@files){
	# Read file into array
	my @lines = read_file($file, chomp => 1);

	# Remove html tags, punctuation, and numbers
	s/<.+?>//g for @lines;
	s/[[:punct:]]/ /g for @lines;
	s/\d//g for @lines;

	# Split into list of unique words
	my @words = uniq(split ' ', join(" ", @lines));

	# Lowercase everything
	$_ = lc for @words;

	# Remove words found in the stop word list
	my %h;
	@h{@stop_words} = undef;
	@words = grep {not exists $h{$_}} @words;

	# Join words into a single string for easy output
	my $word_output = join(",", @words);

	# Remove nonprintable characters
	$word_output =~ s/[[:^print:]\s]//g;

	# Print output to index file
	print $writer "$file,$word_output\n";
}
close $writer;

# Add file name and path to array, only if it is an HTML file
sub wanted {
	if ((split /\./, $File::Find::name)[-1] eq "html"){
		push @files, $File::Find::name;
	}
	return;
}
