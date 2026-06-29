#include "ArpLayer.h"
#include "IpAddress.h"
#include "MacAddress.h"
#include "NetworkUtils.h"
#include "Packet.h"
#include "PcapFileDevice.h"
#include "PcapLiveDevice.h"
#include "PcapLiveDeviceList.h"
#include <iostream>

void create_arp_packet() { pcpp::Packet arpRequest(500); }

pcpp::MacAddress getMacAddress(pcpp::IPv4Address addr,
                               pcpp::PcapLiveDevice *device,
                               double &timeinMili) {
  pcpp::NetworkUtils netUtils = pcpp::NetworkUtils::getInstance();
  return (netUtils.getMacAddress(addr, device, timeinMili));
}

int main() {
  // 192.168.112.236 Maxou
  pcpp::PcapLiveDevice *dev =
      pcpp::PcapLiveDeviceList::getInstance().getDeviceByName("wlp0s20f3");
  pcpp::IPv4Address target("192.168.112.236");
  double lol = 0.0;
  std::cout << "Max mac" << getMacAddress(target, dev, lol) << " In " << lol << " Milisecond";

  // // pcpp::PcapLiveDevice* dev =
  // // pcpp::PcapLiveDeviceList::getInstance().getDeviceByIp(interfaceIPAddr.c_str());
  // pcpp::PcapFileWriterDevice pcapWriter("output.pcap", pcpp::LINKTYPE_ETHERNET);
  // std::cout << dev->getName() << std::endl;
  // std::cout << dev->getIPv4Address() << std::endl;
  // std::cout << dev->getIPv6Address() << std::endl;
  // std::cout << "Mac address " << dev->getMacAddress() << std::endl;
  // std::cout << dev->getLinkType() << std::endl;
  // std::cout << dev->getDeviceType() << std::endl;
}
