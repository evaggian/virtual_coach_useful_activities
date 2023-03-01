# virtual_coach_useful_activities
Virtual coach that proposes preparatory activities for quitting smoking and becoming more physically active.


Based on this Github repository (https://github.com/AmirStudy/Rasa_Deployment) as well as the work by Tom Jacobs (https://github.com/TomJ-EU/rasa/tree/dev).


## Setup on Google Compute Engine

To run this project on a Google Compute Engine, I followed these steps:

	1. Create a Google Compute Engine instance 
	   - Use Ubuntu 20.04.
	   - Make sure that the location is in Europe.
	   - Enable http and https traffic.
	   - Choose a small instance for the start, since you have to pay more for larger instances. I started with an e2-medium machine type and 100GB for the boot disk.
	   - The first 3 months you have some free credit.
	2. Follow the instructions from [here](https://github.com/AmirStudy/Rasa_Deployment) in the sense that you “allow full access to all cloud APIs” on the Google Compute Engine instance. This is shown in this video: https://www.youtube.com/watch?v=qOHszxJsuGs&ab_channel=JiteshGaikwad. Also see this screenshot:
	<img src = "Readme_images/allow_full_access.PNG" width = "500" title="Allowing full access to all cloud APIs.">
	3. Open port 5005 for tcp on the Compute Engine instance:
	<img src = "Readme_images/firewall_rule.PNG" width = "500" title="Creating a firewall rule.">
	<img src = "Readme_images/firewall_rule_0.PNG" width = "500" title="Creating a firewall rule 0.">
	<img src = "Readme_images/firewall_rule_1.PNG" width = "500" title="Creating a firewall rule 1.">
	<img src = "Readme_images/firewall_rule_2.PNG" width = "500" title="Creating a firewall rule 2.">
	4. Follow the instructions from [here](https://github.com/AmirStudy/Rasa_Deployment) for installing Docker on the Google Compute Engine instance. You can do this via the command line that opens after you click on "SSH":
	<img src = "Readme_images/ssh.PNG" width = "500" title="Connect via SSH.">
	5. Install docker-compose on the instance:
	   - I folowed the steps described [here](https://levelup.gitconnected.com/the-easiest-docker-docker-compose-setup-on-compute-engine-ec171c09a29a)
	   - `curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
	   - `chmod +x /usr/local/bin/docker-compose`
	   - You might need to add “sudo” in front of the commands to make them work.
	6. I suggest getting a static IP address for your Google Compute Engine instance:
	   - Follow the instructions here: https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address.
	   - You have to pay for every month, but it is rather cheap.
	7. Make sure you turn off your instance whenever you do not need it, as you are charged for the time that it is up.
	8. Set the IP address of your Google Compute Engine instance in the function `send(message)` in script.js: `url: "http://<your_instance_IP>:5005/webhooks/rest/webhook"`. This is why it helps to have a static IP address.
	9. Start your project with `docker-compose up`.
	10. You can access the frontend from your browser via `http://<your_instance_IP>:3000/?userid=<some_user_id>`.


Some errors I got during the setup:
   - "Couldn't connect to Docker daemon at http+docker://localhost - is it running? If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable“ when running `docker-compose up –-build`.
      - I followed the steps suggested here: https://forums.docker.com/t/couldnt-connect-to-docker-daemon-at-http-docker-localhost-is-it-running/87257/2.
	  - These 2 steps fixed the issue for me:
	     <img src = "Readme_images/error_build.PNG" width = "500" title="docker-compose up --build error.">
		 - Run `sudo docker-compose up –build`. 


## License

Copyright (C) 2023 Delft University of Technology.

Licensed under the Apache License, version 2.0. See LICENSE for details.
