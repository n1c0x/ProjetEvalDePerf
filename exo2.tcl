#create simulator
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

# protocole de routage DV: distance vector LS: link state
$ns rtproto DV

set f [open my.dat w]
$ns trace-all $f
set nf [open out2.nam w]
$ns namtrace-all $nf

#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Execute NAM on the trace file
        exec nam -a out2.nam &
        exit 0
}

for {set i 0} {$i < 6} {incr i} {
	set n($i) [$ns node]
}

$ns duplex-link $n(0) $n(1) 5Mb 10ms DropTail
$ns duplex-link $n(2) $n(1) 5Mb 10ms DropTail

$ns duplex-link $n(3) $n(4) 5Mb 10ms DropTail
$ns duplex-link $n(5) $n(4) 5Mb 10ms DropTail

$ns duplex-link $n(1) $n(4) 0.5Mb 40ms DropTail
$ns duplex-link-op $n(1) $n(4) queuePos 0.5

#Set Queue Size of link (n1-n4) to 10
$ns queue-limit $n(1) $n(4) 10


set tcp1 [new Agent/TCP/Reno]
$ns attach-agent $n(0) $tcp1

set tcp2 [new Agent/TCP/Reno]
$ns attach-agent $n(2) $tcp2


set sink1 [new Agent/TCPSink]
$ns attach-agent $n(3) $sink1
$ns connect $tcp1 $sink1
$tcp1 set fid_ 1

set sink2 [new Agent/TCPSink]
$ns attach-agent $n(5) $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 1


# Setup a FTP traffic generator on "tcp1"
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1
$ftp1 set type_ FTP

# Setup a FTP traffic generator on "tcp2"
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP


# start/stop the traffic
$ns at 0.1 "$ftp1 start"
$ns at 1.0 "$ftp2 start"
$ns at 4.0 "$ftp2 stop"
$ns at 4.5 "$ftp1 stop"

# Set simulation end time
$ns at 5.0 "finish"

# procedure to plot the congestion window
proc plotWindow {tcpSource outfile} {
   global ns
   set now [$ns now]
   set cwnd [$tcpSource set cwnd_]

# the data is recorded in a file called congestion.xg (this can be plotted # using xgraph or gnuplot. this example uses xgraph to plot the cwnd_
   puts  $outfile  "$now $cwnd"
   $ns at [expr $now+0.1] "plotWindow $tcpSource  $outfile"
}

set outfile [open  "congestion.dat"  w]
$ns  at  0.0  "plotWindow $tcp1  $outfile"
#proc finish {} {
 #exec gnuplot congestion.dat -geometry 300x300 &
# exit 0
#}



# Run simulation 
$ns run