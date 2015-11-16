#!/usr/bin/ruby

require "net/http"
require "uri"
require "json"
require "pp"

myhostname = "YOURHOSTNAME"

uri = URI.parse("http://YOURANSIBLETOWER/api/v1/hosts/")

http = Net::HTTP.new(uri.host, uri.port)

request = Net::HTTP::Post.new(uri.request_uri)

request.set_form_data({"name" => myhostname, "inventory" => 2})

request.basic_auth("admin", "YOURPASSWORD")

response = http.request(request)

#formatted = JSON.parse(response.body)
#pp(formatted)
