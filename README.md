# Breck-IndProject

About: This project is about creating a neural network that will be trained on professional chess games in order to be able to beat an average chess player.
        The end goal being a quickly trained AI that has the ability to understand and play chess at a decently high level.
        It is not expected to be the best nor beat the best opponents, but instead hold its own and beat average to higher skilled players.
        I will be importing chess game files and then creating functions using python that can turn the data into understandable matrix's for the neural network to train on.
        The project will be done with python in VSCode, it will only take 1-2 files in total as much can be done in a singular file. 

Tools: The tools needed are VSCode, this is because all of the libraries and inputs will be done inside the VSCode terminal and exist within the extensions of VSCode.
        The tools used are tensorflow, chess, torch, numpy, and tqdm. These are all libraries that can be accessed within python in VSCode.

Build Instructions: In order to build this project you will have to open VSCode and name a file and "name".py. This will create a python file, from here you have to open the VSCode terminal and then open command prompt.
                        Then you have to run the command ' python -m venv "name of virtual environment" ' which will create a new file that is your vitual environment.
                        Next, you have to activate the venv by running the command ' "name of venv" .\venv_name\Scripts\activate '
                        From here you need to install the needed libraries using the command ' pip install torch ' as an example of one of the needed libraries.
                        Now that you have done that, you have the necessary environment needed to run this program. 
                        The data you can get from lichess.com or any other .pgn file that holds chess games as its data.
