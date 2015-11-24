# Mac Asset Tag

## What were we trying to solve?

There are a lot of simple solutions out there for prompting a Mac user for the asset tag to their computer and submitting that value to the JSS. In fact, the jamf binary handles this using the recon option:

```
~$ sudo jamf recon -assetTag XXXXXX
```

A solution for prompting a user can be as simple as using a call to osascript in a shell script or writing it entirely in AppleScript and submitting the value input by the user.

Instead, the asset tag script written for use at JAMF Software became a test ground for what could be done for user interaction through Self Service.

## What does it do?

The script, written in Python, generates a GUI using the Tkinter framework and submits the entered asset tag value to the computer record via the JSS REST API.

The custom GUI that is generated from the script contains an embedded graphic and displays feedback to the user when they click the Submit button. A regular expression is used to ensure what the user enters into the input field matches what we expect for an asset tag.

Message for an invalid asset tag value:

![Screenshot](/images/invalid_tag.png)

Message for an existing asset tag on the record:

![Screenshot](/images/existing_tag.png)

Message for successful update of the asset tag:

![Screenshot](/images/success.png)

If you want to dive into how the GUI is created and defined, you will find the code in the script is heavily commented and should be able to experiment with altering the appearance or crafting your own.

## How to deploy this script in a policy

Upload the script to your JSS and create a policy. Enter the JSS API username into parameter 4 and the password into parameter 5.

This user account will need read/update permissions to **computer** objects and update permissions to **user** objects.

## License

```
JAMF Software Standard License

Copyright (c) 2015, JAMF Software, LLC. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted
provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of
      conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.
    * Neither the name of the JAMF Software, LLC nor the names of its contributors may be
      used to endorse or promote products derived from this software without specific prior
      written permission.

THIS SOFTWARE IS PROVIDED BY JAMF SOFTWARE, LLC "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JAMF SOFTWARE, LLC BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```