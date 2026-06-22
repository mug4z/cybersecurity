#include <iostream>
#include "IPv4Layer.h"
#include "Packet.h"
#include "PcapFileDevice.h"
#include "PcapLiveDeviceList.h"

int main () {
  std::string interfaceIPAddr = "10.84.11.225";

	// find the interface by IP address
	pcpp::PcapLiveDevice* dev = pcpp::PcapLiveDeviceList::getInstance().getDeviceByIp(interfaceIPAddr.c_str());
  pcpp::PcapFileWriterDevice pcapWriter("output.pcap", pcpp::LINKTYPE_FC_2);
  std::cout << dev->getName();

  // try to open the file for writing
  if (!pcapWriter.open())
  {
      std::cerr << "Cannot open output.pcap for writing" << std::endl;
      return 1;
  }
  return 0;
}
