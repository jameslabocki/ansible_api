#!/usr/bin/ruby
# This snippet obtains the ip address of a virtual machine running in RHEV
# There is little to no error checking! :)

require "net/https"
require "uri"
require "json"
require "pp"
require 'rexml/document'

include REXML

vmname = "ose_master"

uri = URI.parse("https://10.19.1.103/api/vms?search=name="+vmname)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth("admin@internal", "100yard-")
response = http.request(request)

doc = Document.new(response.body)

doc.elements.each("vms/vm/guest_info/fqdn") { |element| puts element.text }

# Keeping all this around because it's useful in troubleshooting and/or examples of pulling other information
#doc.elements.each("vms/vm") { |element| puts element.attributes["id"] }
#root = doc.root
#puts root.elements["vms"].attributes["fqdn"]
#fqdn = doc.elements.each("vms/vm/guest_info/fqdn")
#fqdn = doc.elements.each("vms/vm/guest_info/fqdn") { |element| puts element.attributes["fqdn"] }
#puts doc
