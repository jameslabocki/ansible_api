#!/usr/bin/ruby

require 'rest-client'

response = RestClient.post "https://admin:redhat@10.19.1.107/api/v1/jobs/", { 'name' => "BasicScan", "description" => "yesssir3", "project" => "6" }.to_json, :content_type => :json, :accept => :json

print response



