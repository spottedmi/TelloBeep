pipeline{
	agent any


	
	environment {
		
		REMOTE_ADDRESS = credentials('prod_server_address')

		// TAG_NAME = 'latest';
		REPO_USER = "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[-2].toLowerCase()}";
		REPO_NAME = "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/').last().split("\\.")[0].toLowerCase()}";
		
		// REPO = "$REPO_USER/$REPO_NAME";
		REPO = "randomguy090/$REPO_NAME";
		RUN_FOR = "main,develop";
		
		HEARTBEAT_CHECK_INTERVAL=300;
	}

	stages{
	
		stage("Preparing"){
			steps{


				script{

					if (env.BRANCH_NAME == "main"){

						sh 'echo latest > TAG_NAME';
					}else if (env.BRANCH_NAME == "develop"){
						sh 'echo develop > TAG_NAME';

					}else{
						sh "echo ${env.BRANCH_NAME} > TAG_NAME";

					}
					
					 TAG_NAME = readFile('TAG_NAME').trim()					



					echo "$env.BRANCH_NAME";
					echo "$TAG_NAME";
					if( ! env.RUN_FOR.tokenize(",").contains(env.BRANCH_NAME) ) {
						echo "branch is not main";
						currentBuild.result = 'SUCCESS';
						error("wrong branch");
						return
					}
					

					sh "apt update && apt upgrade -y ";
					sh "apt install python3-pip -y ";
					sh "apt install curl -y ";
					
					sh "python3 -m pip install -r requirements.txt";
					sh "apt install docker -y ";

					echo "build tag ${env.BUILD_TAG}";
					echo "repo name: ${scm.getUserRemoteConfigs()[0].getUrl()}"
				}
			}
		}
		stage("Testing"){
			steps{
				script {
					echo "---------------testing---------------";
					echo "list all images built";
					sh "docker images";
					// echo "$IMG";
				}
			}
		}
		stage("Building-Docker"){
			steps{
				script {

					echo "---------------building---------------";
					echo "building docker image via built in function";
					IMG = docker.build("$REPO:$TAG_NAME");
					echo "build image: $IMG";

				}
			}
		}

		stage("Setup-exe"){
			steps{
				script {

					echo "---------------setting up exe ---------------";
					echo "building python package";

					// IMG = docker.build("$REPO:$TAG_NAME");
					// echo "build image: $IMG";
					sh 'ls';

					sh "python3 setup.py build";
					sh "python3 setup.py install";


				}
			}
		}
		stage("Building-exe"){
			steps{
				script {

					echo "---------------building exe ---------------";
					echo "building exe image via built in function";
					sh 'ls';
					sh "python3 -m pip install pyinstaller"
					sh 'pyinstaller --onefile  --hidden-import=TelloBeep --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=packaging.utils run.py'
					sh 'ls';
					sh 'ls dist/run';

				}
			}
		}
		stage("release"){
			steps{	
				script {
					withCredentials([usernamePassword(credentialsId: "github_token", passwordVariable: 'githubSecret', usernameVariable: 'githubUser')]) {
							sh "cp dist/run run.exe"
							sh "curl https://raw.githubusercontent.com/RandomGuy090/github-auto-release/main/auto-release.sh > run.sh";
							sh "bash run.sh -u spottedmi -r TelloBeep -t $githubSecret -b $TAG_NAME -e run.exe  > VERSION"
							VERSION = readFile('VERSION').trim()
							echo VERSION;					
							echo VERSION;					

						}
					

				}
			}
		}
		stage('Docker Push') {
			steps {
				script{
					echo "---------------pushing to docker hub---------------";

					withCredentials([usernamePassword(credentialsId: "docker_token", passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
					echo "deploying: $IMG:latest";
					IMG.push(TAG_NAME);
					// sh "docker rmi $IMG.id"
						
					}
					withCredentials([usernamePassword(credentialsId: "docker_token", passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
						echo "deploying: $IMG:$VERSION";
						IMG.push(VERSION);
						sh "docker rmi $IMG.id"
							
					}
				}
			} 
		}
		stage("deploy"){
			steps{	
				script {
					command = "docker compose  -f /home/randomguy90/Desktop/spotted/tellobeep/docker-compose.yml restart"
					// withCredentials([string(credentialsId: 'prod_server_address', variable: 'ADDRESS}')]) {
					// 	withCredentials([sshUserPrivateKey(credentialsId: 'ssh_server', keyFileVariable: 'SSH_KEY_PATH', passphraseVariable: 'PASS', usernameVariable: 'SSH_USER')]) {
					// 		sshagent() {
					// 			sshCommand remote: '$ADDRESS', user: "$SSH_USER", command: "$command", password: "$PASS"
					// 		}
					// 	}
					// }
					
					sshagent(credentials: ['ssh_server']) {
						sh 'ssh -o StrictHostKeyChecking=no jenkins_minion@${REMOTE_ADDRESS} uptime'
						sh "ssh -v jenkins_minion@${REMOTE_ADDRESS}  'docker compose  -f /home/randomguy90/Desktop/spotted/tellobeep/docker-compose.yml restart'";
					}
					
					currentBuild.result = 'SUCCESS'
					return
				}
			}
		}
	}
}