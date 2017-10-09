# Trained by Demonstration NAO Robot Controlled via a BCI system for Telepresence

Nao robot learning, control and BCI event listener script. Should be run together with Buffer BCI (FieldTrip). Events from the Buffer will be catched by Python script and control signal will be sent to the robot. Robot training stage is at the beginning of script. User can perform as much demos as wants, however learning time will be increased. In general 3 demonstrations are sufficient for smooth reproduction. Also, 15 gaussian states is used to fit gaussian model, this number can be changed in NAO class contructor.

# Installation

Just clone or download this project.
Following packages have to be installed: numpy <1.12.1>, matplotlib <2.0.0>, fastdtw <0.3.0>, scipy <0.16.1>. Also, NAO robot control framework 'naoqi' should be installed. 

# NAO humanoid robot

<p align="center">
  <img width="35%" height="35%" src="https://raw.githubusercontent.com/BatyaGG/Trained-by-Demonstration-NAO-Robot-Controlled-via-a-BCI-system-for-Telepresence/master/NAO.jpg">
</p>

NAO is a humanoid robot developed by Aldebaran Robotics french company. It is 59cm tall robot which is designed for different aims, however mostly used in academic side. Having 25 degrees of freedom NAO can perform various, complex body motions. The robot is one of common robots used in telepresence topic since several advantages of the robot. The robot is equipped with numerous sensors in its head, body, feet and hands allowing robot to perceive its environment and perform tasks respectively. Also, NAO have several 4 directional microphones and loudspeakers to interact with humans in effectively essential manner. NAO sees world using 2 high resolution cameras and able to recognize various shapes and objects and connects to Internet through Ethernet or WiFi. All these advantages improve the effect of operator presence and alleviate robot control process.

# System Architecture

<p align="center">
  <img width="75%" height="75%" src="https://raw.githubusercontent.com/BatyaGG/Trained-by-Demonstration-NAO-Robot-Controlled-via-a-BCI-system-for-Telepresence/master/Architecture.png">
</p>

Overall system flow is managed by Fieldtrip Buffer which regulates BCI and NAO robot control systems, handles and sends events. Subject interacts with P300 graphical user interface and gets feedback from NAO robot in a form of video and audio stream. Calibration is requested by BCI system at the beginning, signal processing is performed on raw EEG, the model is trained and stored in the buffer for current session. At testing stage BCI model classifies processed EEG data and the buffer handles events on a real-time basis. Events are continuously listened by NAO control script implemented on Python. The script avoids events stacking to improve real-time response of the system, i.e. in case 2 events came one after another, script will execute only first event and will ignore any other events till NAO finishes current task. Moreover, we do not need to train the NAO before BCI session, since BCI and PbD models are independent of each other. NAO can be retrained anytime, even while BCI session holds on. In such case, at the next call of that event, NAO will perform retrained new action. Training is done using Gaussian Mixture Models technique from PbD field, where Gaussian Mixture Regression for end-effector motion is found from demonstrations and performed by the robot.

# Programming by demonstration

Programming by demonstration (PbD) is a robotics field developing methods for teaching robots by showing to them how to perform a particular task. Such methodoly of programming is user-friendly and do not require any programming skills or knowledge of programming languages. This is very useful mechanism of teaching robots which decreases their costs, since factories will be able to produce only general robots, which can be programmed in any way a buyer wants. Current PbD approach is based on Gaussian Mixture Models (GMM) soft clustering algorithm which considers data as finite gaussian distributions with unknown parameters. Expectation-Maximization (EM) algorithm is used to find gaussian states parameters which is iterative algorithm which converges to true gaussian parameters and stopped by log-likelihood threshold or iteration number limit. To initialize gaussian parameters k-means clustering algorithm is used. After GMM is fitted, the model is used to fit Gaussian Mixture Regression (GMR) to retrieve robot arm trajectories by time input. GMM/GMR functions are from my [Gaussian-Mixture-Models project](https://github.com/BatyaGG/Gaussian-Mixture-Models), please check it out.

# Dynamic Time Warping

<p align="center">
  <img width="90%" height="90%" src="https://raw.githubusercontent.com/BatyaGG/Trained-by-Demonstration-NAO-Robot-Controlled-via-a-BCI-system-for-Telepresence/master/figure_trajectory.png">
</p>

All demonstrations are aligned to first demonstration by similarities in trajectories using Dynamic Time Warping (DTW) algorithm. This is done to sustain the shape of trajectory, since different demonstration speeds will lead to cluster mess. Above figure demonstration trajectories are already fitted by DTW algorithm. It can be seen from ideal demonstration trajectories that run over each other in x-axis and z-axis trajectory and y-axis orientation subplots. Y-axis and x-axis trajectories and z-axis orientations had different values each demonstration, but still matched as much as possible. Purple puddles shows variance of trajectories, blue line shows regression line and light blue lines are demonstration trajectories.

