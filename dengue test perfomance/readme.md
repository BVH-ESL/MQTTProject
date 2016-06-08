<h1>Usage of dengue for test MQTT broker</h1>
<h2>Broker file</h2>
<ul>
  <li>check_usage.py - check cpu, cpu temp, ram of MQTT process </li>
  <li>Command - python check_usage.py -pid MQTTprocessid</li>
</ul>
<h2>Published file</h2>
<ul>
  <li>dengue_pub_v2.py - waiting command form subscriber and publish msg follow msg rate form subscriber in 5 Min</li>
  <li>Command - python dengue_pub_v2.py --rpid yourPubid</li>
</ul>
<h2>Subscriber file</h2>
<ul>
  <li>dengue_sub_v2.py - send scan command to published wait and send start command, waiting for last msg and summary result</li>
  <li>Command - python dengue_sub_v2.py -C yourConnectionRate</li>
</ul>
