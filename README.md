# Trained by Demonstration NAO Robot Controlled via a BCI system for Telepresence

# NAO humanoid robot

<p align="center">
  <img width="150" height="150" src="https://raw.githubusercontent.com/BatyaGG/Trained-by-Demonstration-NAO-Robot-Controlled-via-a-BCI-system-for-Telepresence/master/NAO.jpg">
</p>

NAO is a humanoid robot developed by Aldebaran Robotics french company. It is 59cm tall robot which is designed for different aims, however mostly used in academic side. Having 25 degrees of freedom NAO can perform various, complex body motions. The robot is one of common robots used in telepresence topic since several advantages of the robot. The robot is equipped with numerous sensors in its head, body, feet and hands allowing robot to perceive its environment and perform tasks respectively. Also, NAO have several 4 directional microphones and loudspeakers to interact with humans in effectively essential manner. NAO sees world using 2 high resolution cameras and able to recognize various shapes and objects and connects to Internet through Ethernet or WiFi. All these advantages improve the effect of operator presence and alleviate robot control process.

# System Architecture
Overall system flow is managed by Fieldtrip Buffer which regulates BCI and NAO robot control systems, handles and sends events. Subject interacts with P300 graphical user interface and gets feedback from NAO robot in a form of video and audio stream. Calibration is requested by BCI system at the beginning, signal processing is performed on raw EEG, the model is trained and stored in the buffer for current session. At testing stage BCI model classifies processed EEG data and the buffer handles events on a real-time basis. Events are continuously listened by NAO control script implemented on Python. The script avoids events stacking to improve real-time response of the system, i.e. in case 2 events came one after another, script will execute only first event and will ignore any other events till NAO finishes current task. Moreover, we do not need to train the NAO before BCI session, since BCI and PbD models are independent of each other. NAO can be retrained anytime, even while BCI session holds on. In such case, at the next call of that event, NAO will perform retrained new action. Training is done using Gaussian Mixture Models technique from PbD field, where Gaussian Mixture Regression for end-effector motion is found from demonstrations and performed by the robot.

