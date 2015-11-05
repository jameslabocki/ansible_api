#!/usr/bin/ruby

require "net/http"
require "uri"
require "json"
require "pp"

uri = URI.parse("http://10.19.1.107/api/v1/hosts/")

http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth("admin", "redhat")
response = http.request(request)

formatted = JSON.parse(response.body)

pp(formatted)
