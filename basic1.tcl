Class TraceApp -superclass Application

#Create a simulator object
set ns [new Simulator]

#Open the nam file basic1.nam and the variable-trace file basic1.tr
set namfile [open basic1.nam w]
$ns namtrace-all $namfile
set tracefile [open basic1.tr w]
$ns trace-all $tracefile

#Define a 'finish' procedure
proc finish {} {
        global ns namfile tracefile
        $ns flush-trace
        close $namfile
        close $tracefile
	exec nam basic1.nam &
        exit 0
	exit 1
}

#Create the network nodes
set N1 [$ns node]
set N2 [$ns node]
set R0 [$ns node]
set R1 [$ns node]
set N5 [$ns node]
set N6 [$ns node]

#Create a duplex link between the nodes
proc rand_range { min max } { return [expr int(rand() * ($max - $min)) + $min] }

set rand_delay0 [new RandomVariable/Uniform];
$rand_delay0 set min_ 5ms
$rand_delay0 set max_ 25ms

set rand_delay1 [new RandomVariable/Uniform];
$rand_delay1 set min_ 5ms
$rand_delay1 set max_ 25ms

$ns duplex-link $N1 $R0 100Mb 5ms DropTail
$ns duplex-link $R0 $N2 100Mb $rand_delay0 DropTail
$ns duplex-link $N5 $R1 100Mb 5ms DropTail
$ns duplex-link $R1 $N6 100Mb $rand_delay1 DropTail
$ns duplex-link $R0 $R1 100Kb 1ms DropTail

# The queue size at $R is to be 7, including the packet being sent
$ns queue-limit $R0 $R1 10

# some hints for nam
# color packets of flow 0 red
$ns color 0 Red
$ns duplex-link-op $N1 $R0 orient right-down
$ns duplex-link-op $N2 $R0 orient right-up
$ns duplex-link-op $R0 $R1 orient right
$ns duplex-link-op $R1 $N5 orient right-up
$ns duplex-link-op $R1 $N6 orient right-down

$ns color 1 Blue
#$ns color 1 Blue
#$ns duplex-link-op $N5 $R0 orient right
#$ns duplex-link-op $R1 $N6 orient right
#$ns duplex-link-op $R1 $N6 queuePos 0.5

# Create a TCP sending agent and attach it to A
set tcp0 [new Agent/TCP/Newreno]
set tcp1 [new Agent/TCP/Newreno]
# We make our one-and-only flow be flow 0
$tcp0 set class_ 0
$tcp0 set ttl_ 64
#$tcp0 set window_ 20
#$tcp0 set packetSize_ 960
$ns attach-agent $N1 $tcp0

$tcp1 set class_ 1
$tcp1 set ttl_ 64
#$tcp0 set window_ 100
#$tcp1 set packetSize_ 960
$ns attach-agent $N2 $tcp1

# Let's trace some variables
$tcp0 attach $tracefile
$tcp0 tracevar cwnd_
$tcp0 tracevar bytes_
#$tcp0 tracevar ssthresh_
#$tcp0 tracevar ack_
#$tcp0 tracevar maxseq_

#Create a TCP receive agent (a traffic sink) and attach it to B
set end0 [new Agent/TCPSink]
$ns attach-agent $N5 $end0


set end1 [new Agent/TCPSink]
$ns attach-agent $N6 $end1

set traceapp [new TraceApp]
$traceapp attach-agent $end0
$ns  at  0.0  "$traceapp  start"


#Connect the traffic source with the traffic sink
$ns connect $tcp0 $end0

$ns connect $tcp1 $end1

#Schedule the connection data flow; start sending data at T=0, stop at T=10.0
set myftp [new Application/FTP]
$myftp attach-agent $tcp0

set myftp1 [new Application/FTP]
$myftp1 attach-agent $tcp1

$ns at 0.0 "$myftp start"
$ns at 0.0 "$myftp1 start"
$ns at 100.0 "finish"

proc plotWindow {tcpSource outfile} {
     global ns
     set now [$ns now]
     set cwnd [$tcpSource set cwnd_] 
     puts  $outfile  "$now, $cwnd"
     $ns at [expr $now+1.0] "plotWindow  $tcpSource  $outfile"
}
set outfile1  [open  "tcp0_Tahoe_CWND"  w]
$ns  at  0.0  "plotWindow $tcp0  $outfile1"
set outfile3  [open  "tcp1_Tahoe_CWND"  w]
$ns  at  0.0  "plotWindow $tcp1  $outfile3"


proc plotThroughput {tcpSink outfile} {
      global ns
      set now [$ns now];
      set nbytes [$tcpSink set bytes_];
      $tcpSink set bytes_ 0
      set throughput [expr ($nbytes * 8.0 / 1000000) / 1.0]
      puts  $outfile  "$now, $throughput"
      $ns at [expr $now+1.0] "plotThroughput $tcpSink  $outfile"
}

set outfile2  [open  "tcp0_Tahoe_goodput"  w]
$ns  at  0.0  "plotThroughput $end0  $outfile2"
set outfile2  [open  "tcp1_Tahoe_goodput"  w]
$ns  at  0.0  "plotThroughput $end1  $outfile2"

#Run the simulation
$ns run
