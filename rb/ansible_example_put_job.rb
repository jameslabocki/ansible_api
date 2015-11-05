#!/usr/bin/ruby
# This snippet creates a job in ansible tower and then starts it.
# You'll need to replace the set_form_data with the appropriate playbook, project, etc
# It has little to no error checking! 

require "net/https"
require "uri"
require "json"
require "pp"
require "rexml/document"

include REXML

# Create a job in Ansible
# This should probably use a job template, but I took a shortcut
uri = URI.parse("https://10.19.1.107/api/v1/jobs/")
http = Net::HTTP.new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.request_uri)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request.set_form_data name: 'installApache', description: 'yessir3', project: "6", playbook: "webserver.yml", inventory: "2", job_type: "run", credential: "3"
request.basic_auth("admin", "redhat")
response = http.request(request)

# This is useful for troubleshooting
#puts response.body
#print "\n\n"

# Make the response JSON and pull the hash value where key is equal to "id"
newhash = JSON.parse(response.body)
myjobid = newhash["id"].to_s

# Now let's start the job we created
uri = URI.parse("https://10.19.1.107/api/v1/jobs/"+myjobid+"/start/")
http = Net::HTTP.new(uri.host, uri.port)

request = Net::HTTP::Post.new(uri.request_uri)

http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request.set_form_data forks: '0'
request.basic_auth("admin", "redhat")
response = http.request(request)






