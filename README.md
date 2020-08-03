# Contact Tracker 

Contact Tracker is a mobile app for keeping track of possible exposure to
COVID-19 while allowing its users to remain largely anonymous. On its main
screen is displays a large QR code. This code contains a URL pointing back to
the Content Tracker website. The URL contains a unique random number which
identifies the user.

Users scan one another's codes in order to record the fact that they met in
person on a particular day. If one of them later discovers that he has
COVID-19, he can can use this app to inform everyone with whom he came in
contact in the days leading up to the diagnose. They will be informed of the
date on which they came in contact with an infected person but not which person
it was. They may then decide to seek medical advice, a COVID-19 test, or to
self quarantine.

While Contact Tracker does not know the name of the person reporting an
infection, perfect anonymity is not guaranteed. In some cases the recipients of
a notice may be able to infer the identity of the infected person was using
information from outside the app such as their recollections of whom they met
on a certain day. The app is designed to act as a discrete go-between,
collecting and passing on only the bare minimum of information they need to
slow the spread of the disease.

## Authors

The Contact Tracker concept and theory of operation were devised by Mykhaylo
Telychko. The Demo Implementation described below was written by David Chappell.
Feel free to contact them by opening an Issue on the project's Github page:
<https://github.com/david672orford/contact-tracker>.

## Demo Implementation

We provide a simple implementation of the Contact Tracker mobile app concept.
It takes the form of a mobile website using the Python Flask framework. The
mobile site is written as a Progressive Web App (PWA) which means that it can
be installed on the phone as an application.

### Copyright and License to the Demo Implementation

Copyright 2020 David Chappell

Content Tracker is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

Content Tracker is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Contact Tracker. If not, see <https://www.gnu.org/licenses/>.

### Third Party Software in the Demo Implementation

The QR code scanner used in this project comes from
<https://github.com/nimiq/qr-scanner>. It is the version which was posted
there on 15 July 2020.

### Possible Improvements to the Demo Implementation

* There should be a way to dismiss the "Scan Recorded" message which
  appears underneath the QR code after one scans another user's code
* The CSS rules which adjust the size of the QR code to the size
  of the device's screen are a hack. They do not take proper account
  of the amount of available vertical space.
* We need to consider the possibility that users might spam the server
  with false contact reports: 1) They could reuse QR codes they had scanned
  before to report new false contacts. To prevent this we could put the
  date in the code and cryptographically sign it. 2) They could attempt
  to guess codes in order to report contact with people whom they had
  not met at all. Since the code space is large, it might be sufficient
  to rate limit.
* Currently users must open the app and go to the proper tab to see
  notifications. We should: 1) provide a visual indication on the tab bar
  and 2) implement push notifications.
* The service worker does not cache the main page. This is because it
  changes in response to POST requests to other URL's. We can either
  retrieve changing parts using AJAX or we can cache it and invalidate
  the cache whenever a POST request is sent.
* With suitable improvements to the service worker, the user could scan
  while offline and the contact reports would be uploaded when he went
  on line.

