# Secret Santa Communication
 A secret santa event communications system. Respects secret santa anonymity by implementing a sms proxy number and GPT-3 based message translator to sound as if it was written by a child or santa, depending on who the user is texting. 

## Examples
<br><img src="https://user-images.githubusercontent.com/72144488/148700190-319d7825-6bf1-4859-8b82-069ab53c5637.PNG" alt="screenshot" width="400"/><br>
This shows an example from the perspective of a user texting their secret santa. A text from the santa is shown in the "Santa:..." message. When the user responds, the system shows how their message was translated and sent to the santa in the 'You:..." message. The system uses OpenAI's GPT-3 API to reword the text to a todler's manner of speaking as it is being sent from the "child" to the secret santa.
<br><br>
<br><img src="https://user-images.githubusercontent.com/72144488/148700653-e0f52660-b331-4603-827a-efca5d114a3e.PNG" alt="screenshot" width="400"/><br>
From the other perspective, a santa texting their child can see the childs name and their messages are translated to sound like they are from Santa.
