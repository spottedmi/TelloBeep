pipeline{
	agent any
	
	environment {
		
		// TAG_NAME = 'latest';
		REPO_USER = "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[-2].toLowerCase()}";
		REPO_NAME = "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/').last().split("\\.")[0]}";
		
		REPO = "$REPO_USER/$REPO_NAME";
		RUN_FOR = "main,develop";
		
	}

	stages{
		stage("Preparing"){
			steps{


				script{


					if (env.BRANCH_NAME == "main"){

						sh 'echo latest > TAG_NAME';
					}

					if (env.BRANCH_NAME == "develop"){
						sh 'echo develop > TAG_NAME';

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
					
					sh "python3 -m pip install -r requirements.txt";
					sh "apt install docker -y ";

					echo "build tag ${env.BUILD_TAG}";
					echo "repo name: ${scm.getUserRemoteConfigs()[0].getUrl()}"
				}
			}
		}
		stage("Building"){
			steps{
				script {

					echo "---------------building---------------";
					echo "building docker image via built in function";
					IMG = docker.build("$REPO:$TAG_NAME");
					echo "build image: $IMG";

				}
			}
		}
		stage("Testing"){
			steps{
				script {
					echo "---------------testing---------------";
					echo "list all images built";
					sh "docker images";
					echo "$IMG";
				}
			}
		}
		stage('Docker Push') {
			      steps {
				      script{
						echo "---------------pushing to docker hub---------------";

					      withCredentials([usernamePassword(credentialsId: "docker_token", passwordVariable: 'dockerHubPassword', usernameVariable: 'dockerHubUser')]) {
							echo "deploying: $IMG";
							IMG.push(TAG_NAME);
							sh "docker rmi $IMG.id"
						      
						}
					}
			    } 
		}
		

		stage("deploy"){
			steps{	
				script {
					echo "---------------deploying---------------";

				}
			}
		}
		
		stage("release"){
			steps{	
				script {
					withCredentials([usernamePassword(credentialsId: "github_token", passwordVariable: 'githubSecret', usernameVariable: 'githubUser')]) {
							sh "curl https://raw.githubusercontent.com/RandomGuy090/github-auto-release/main/auto-release.sh > run.sh";

							if( env.BRANCH_NAME == "main"){
								sh "bash run.sh -r https://api.github.com/repos/RandomGuy090/testing/releases -t $githubSecret "
							}else{
								sh "bash run.sh -r https://api.github.com/repos/RandomGuy090/testing/releases -t $githubSecret -p "
							}
						}
					

				}
			}
		}
		
	}
}
