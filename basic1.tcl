set protocol $argv
set ns [new Simulator]
set tracefile [open $protocol.tr w]
$ns trace-all $tracefile

proc finish {} {
        global ns tracefile
        $ns flush-trace
        close $tracefile
        exit 0
	exit 1
}

#-------------------------------------------------------------------------------------------------------
# create the network nodes
set N1 [$ns node]
set N2 [$ns node]
set R0 [$ns node]
set R1 [$ns node]
set N5 [$ns node]
set N6 [$ns node]
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# generating those random variables for random delays
set rand_delay0 [new RandomVariable/Uniform];
$rand_delay0 set min_ 5ms
$rand_delay0 set max_ 25ms

set rand_delay1 [new RandomVariable/Uniform];
$rand_delay1 set min_ 5ms
$rand_delay1 set max_ 25ms
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# defining the links and their speed - delay - types etc...
$ns duplex-link $N1 $R0 100Mb 5ms DropTail
$ns duplex-link $R0 $N2 100Mb $rand_delay0 DropTail
$ns duplex-link $N5 $R1 100Mb 5ms DropTail
$ns duplex-link $R1 $N6 100Mb $rand_delay1 DropTail
$ns duplex-link $R0 $R1 100Kb 1ms DropTail
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# for routers buffers
$ns queue-limit $R0 $R1 10
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# creating tcp agents and setting congestion control protocol
set tcp0 [new Agent/$protocol]
$tcp0 set class_ 0
$tcp0 set ttl_ 64
$ns attach-agent $N1 $tcp0

set tcp1 [new Agent/$protocol]
$tcp1 set class_ 1
$tcp1 set ttl_ 64
$ns attach-agent $N2 $tcp1
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# variables that we are tracing
$tcp0 attach $tracefile
$tcp0 tracevar cwnd_
$tcp0 tracevar ack_
$tcp0 tracevar rtt_

$tcp1 attach $tracefile
$tcp1 tracevar cwnd_
$tcp1 tracevar ack_
$tcp1 tracevar rtt_
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# tcp recieve agents
set end0 [new Agent/TCPSink]
$ns attach-agent $N5 $end0

set end1 [new Agent/TCPSink]
$ns attach-agent $N6 $end1
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# connecting ends
$ns connect $tcp0 $end0
$ns connect $tcp1 $end1
#-------------------------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------------------------
# creating a data stream into connections and setting start and finish time
set myftp0 [new Application/FTP]
$myftp0 attach-agent $tcp0

set myftp1 [new Application/FTP]
$myftp1 attach-agent $tcp1
#-------------------------------------------------------------------------------------------------------

$ns at 0.0 "$myftp0 start"
$ns at 0.0 "$myftp1 start"
$ns at 1000.0 "finish"

# run!
$ns run
