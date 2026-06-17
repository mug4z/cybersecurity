#include <iostream>
#include "/home/tfrily/.brew/opt/pcapplusplus/include/pcapplusplus/IPv4Layer.h"
#include "/home/tfrily/.brew/opt/pcapplusplus/include/pcapplusplus/Packet.h"
#include "/home/tfrily/.brew/opt/pcapplusplus/include/pcapplusplus/PcapFileDevice.h"

int main (int argc, char *argv[]) {
  
  pcpp::PcapFileWriterDevice pcapWriter("output.pcap", pcpp::LINKTYPE_ETHERNET);

  // try to open the file for writing
  if (!pcapWriter.open())
  {
      std::cerr << "Cannot open output.pcap for writing" << std::endl;
      return 1;
  }
  return 0;
}
