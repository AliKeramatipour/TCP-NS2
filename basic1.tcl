set protocol $argv
set ns [new Simulator]
set namfile [open $protocol.nam w]
$ns namtrace-all $namfile
set tracefile [open $protocol.tr w]
#$ns trace-all $tracefile

proc finish {} {
        global ns namfile tracefile
        $ns flush-trace
        close $namfile
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
# designing the nam animation look
$ns color 0 Red
$ns color 1 Blue

$ns duplex-link-op $N1 $R0 orient right-down
$ns duplex-link-op $N2 $R0 orient right-up
$ns duplex-link-op $R0 $R1 orient right
$ns duplex-link-op $R1 $N5 orient right-up
$ns duplex-link-op $R1 $N6 orient right-down
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# creating tcp agents and setting congestion control protocol
set tcp0 [new Agent/TCP/$protocol]
$tcp0 set class_ 0
$tcp0 set ttl_ 64
$ns attach-agent $N1 $tcp0

set tcp1 [new Agent/TCP/$protocol]
$tcp1 set class_ 1
$tcp1 set ttl_ 64
$ns attach-agent $N2 $tcp1
#-------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------
# variables that we are tracing
$tcp0 attach $tracefile
$tcp0 tracevar cwnd_
$tcp0 tracevar ack_

$tcp1 attach $tracefile
$tcp1 tracevar cwnd_
$tcp1 tracevar ack_
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
$ns at 100.0 "finish"

# run!
$ns run
