
#include "ArpLayer.h"
#include "IpAddress.h"
#include "MacAddress.h"
#include "NetworkUtils.h"
#include "Packet.h"
#include "PcapFileDevice.h"
#include "PcapLiveDevice.h"
#include "PcapLiveDeviceList.h"
#include "SystemUtils.h"
#include <cstdlib>
#include <getopt.h>
#include <iostream>

void create_arp_packet() { pcpp::Packet arpRequest(500); }

pcpp::MacAddress getMacAddress(pcpp::IPv4Address addr,
                               pcpp::PcapLiveDevice *device,
                               double &timeinMili) {
  pcpp::NetworkUtils netUtils = pcpp::NetworkUtils::getInstance();
  return (netUtils.getMacAddress(addr, device, timeinMili));
}

int main(int argc, char **argv) {

  pcpp::AppName::init(argc, argv);

  if (argc < 5) {
    std::cout << "Not enough arguments" << std::endl;
    exit(1);
  }

  std::string ip_src = argv[1], mac_src = argv[2], ip_target = argv[3],
              mac_target = argv[4];

  if (ip_src == "" || mac_src == "" || ip_target == "" || mac_target == "") {

    std::cout << "Please give source ip/mac and target ip/mac" << std::endl;
    exit(1);
  }

  pcpp::IPv4Address IPv4_source;
  // pcpp::MacAddress MAC_source;
  // pcpp::IPv4Address IPv4_target;
  // pcpp::MacAddress MAC_target;

  try {

    IPv4_source = pcpp::IPv4Address(ip_src);

  } catch (const std::exception &) {
    std::cout << "Ip source not valid" << std::endl;
    exit(1);
  }
  pcpp::PcapLiveDevice *pIfaceDevice =
      pcpp::PcapLiveDeviceList::getInstance().getDeviceByIp(IPv4_source);
  std::cout << pIfaceDevice->getName() << std::endl;

  if (pIfaceDevice == nullptr) {
    std::cout << "Cannot find interface " << std::endl;
    exit(1);
  }
}

// TODO: Create an eth and arplayer
// TODO: Create
