#!/usr/bin/ruby

require "net/http"
require "uri"
require "json"
require "pp"

uri = URI.parse("http://YOURTOWERAPI/api/v1/hosts/")

http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Get.new(uri.request_uri)
request.basic_auth("admin", "YOURPASSWORD")
response = http.request(request)

formatted = JSON.parse(response.body)

pp(formatted)
