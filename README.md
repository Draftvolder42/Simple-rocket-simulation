# [Simple rocket flight simulation]
**Simple rocket flight simulation with proportional navigation algorithm.**

---

### **[CONTENT]**
We have a rocket ( **$`\textcolor{blue}{\text{blue circle}}`$** ) and a target ( **$`\textcolor{red}{\text{red circle}}`$** ), the lines in this circles show the vector of moving.
All params you can change inside `main()` function.

---

> **ROCKET PARAMS** : <br>
<ul>
   <li> <p> <h3> rocket_fov </h3> - rocket field of view <strong> float(degrees) </strong> in both sides | default values is 22.5. </p> </li>
   <li> <p> <h3> rocket_range </h3> - rocket lock range <strong>float()</strong> | default values is 500. </p> </li>
   <li> <p> <h3> maneuverability </h3> - rocket maneuverability <strong>float()</strong> | default values is 2.5. </p> </li>
   <li> <p> <h3> rocket_speed </h3> - speed of rocket <strong>float()</strong> | default values is 140. </p> </li>
</ul>

---

> **PLANE PARAMS** : <br>
<ul>
   <li> <p> <h3> random_turn_mode </h3> - change mode between rocket random turns or keyboard inputs <strong>bool()</strong>. </p> </li>
   <li> <p> <h3> plane_maneuverability </h3> - plane maneuverability <strong>float()</strong> | default values is 1. </p> </li>
   <li> <p> <h3> plane_speed </h3> - speed of plane <strong>float()</strong> | default values is 70. </p> </li>
</ul>

---
> **OPTIONS** : <br>

<ul>
   <li> <p> <h3> fps </h3> - you can change fps <strong>int()</strong>. </p> </li>
   <li> <p> <h3> Rocket have noise </h3> - noisy target coordinates, depending on the distance, will be sent to the rocket. </p> </li>
   <li> <p> <h3> Rocket have a radar fov </h3> - if target outside the radar sector, coordinates will be sent to the rocket from a possible guidance means with corresponding noise. </p> </li>
</ul>



