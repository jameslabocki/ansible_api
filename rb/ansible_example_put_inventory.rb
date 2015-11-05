#!/usr/bin/ruby

require "net/http"
require "uri"
require "json"
require "pp"

uri = URI.parse("http://10.19.1.107/api/v1/hosts/")

http = Net::HTTP.new(uri.host, uri.port)

request = Net::HTTP::Post.new(uri.request_uri)

request.set_form_data({"name" => "newhost2", "inventory" => 1})

request.basic_auth("admin", "redhat")

response = http.request(request)

formatted = JSON.parse(response.body)

pp(formatted)
