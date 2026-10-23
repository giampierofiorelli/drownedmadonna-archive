/**
 * @package JFBConnect
 * @copyright (C) 2009-2011 by Source Coast - All rights reserved
 * @license http://www.gnu.org/licenses/gpl-2.0.html GNU/GPL
 */
var jfbc = {
    login: {
        // login_custom is used for non XFBML login requests (custom image buttons)
        login_custom: function()
        {
            FB.login(function (response)
            {
                if (response.status === 'connected')
                {
                    jfbc.login.login_button_click();
                }
            }, {
                scope: jfbcRequiredPermissions
            });

        },
        // Action to perform after authentication on FB has occurred
        login_button_click: function()
        {
            FB.getLoginStatus(function(response)
            {
                if (response.status === 'connected')
                {
                    self.location = jfbcOptionsPermsUrl;
                }
            });
        },

        logout_button_click: function()
        {
            if (jfbcLogoutFacebook)
            {
                FB.getLoginStatus(function(response)
                {
                    if (response.status === 'connected')
                    {
                        FB.logout(function(response) {
                            jfbc.login.redirect_to_logout();
                        });
                    }
                    else
                    {
                        jfbc.login.redirect_to_logout();
                    }
                });
            }
            else
            {
                jfbc.login.redirect_to_logout();
            }
        },

        redirect_to_logout: function ()
        {
            self.location = jfbcBase + 'index.php?option=com_jfbconnect&task=logout';
        }
    },

    register: {
        checkUsernameAvailable: function()
        {
            var testName = $('username').value;
            if (testName != '')
                var myXHR = new XHR({
                    method:'get',
                    onSuccess:jfbc.register.showUsernameSuccess
                }).send('index.php', 'option=com_jfbconnect&view=loginregister&task=checkUsernameAvailable&username=' + testName);
        },

        checkPassword: function()
        {
            var testPassword = $('password').value;
            var passwordSuccessElement = $('jfbcPasswordSuccess');
            var val = "";
            if (testPassword.length < 6)
                val = '<img src="' + jfbcRoot + 'images/cancel_f2.png" width="20" height="20">' + jfbcPasswordInvalid;
            passwordSuccessElement.innerHTML = val;
        },

        checkPassword2: function()
        {
            var testPassword = $('password').value;
            var testPassword2 = $('password2').value;
            var passwordSuccessElement = $('jfbcPassword2Success');
            var val = "";
            if (testPassword != testPassword2)
                val = '<img src="' + jfbcRoot + 'images/cancel_f2.png" width="20" height="20">' + jfbcPassword2NoMatch;
            passwordSuccessElement.innerHTML = val;
        },

        showUsernameSuccess: function(req)
        {
            var usernameSuccessElement = $('jfbcUsernameSuccess');
            if (req == 1)
            {
                usernameSuccessElement.innerHTML = '<img src="' + jfbcRoot + 'images/apply_f2.png" width="20" height="20">' + jfbcUsernameIsAvailable;
            }
            else
            {
                usernameSuccessElement.innerHTML = '<img src="' + jfbcRoot + 'images/cancel_f2.png" width="20" height="20">' + jfbcUsernameIsInUse;
            }

        },

        checkEmailAvailable: function()
        {
            var testEmail = $('email').value;
            if (testEmail != '' && jfbc.register.isEmail(testEmail))
                var myXHR = new XHR({
                    method:'get',
                    onSuccess:jfbc.register.showEmailSuccess
                }).send('index.php', 'option=com_jfbconnect&view=loginregister&task=checkEmailAvailable&email=' + testEmail);
        },

        showEmailSuccess: function(req)
        {
            emailSuccessElement = document.getElementById('jfbcEmailSuccess');
            if (req == 1)
            {
                emailSuccessElement.innerHTML = '<img src="' + jfbcRoot + 'images/apply_f2.png" width="20" height="20">' + jfbcEmailIsAvailable;
            }
            else
            {
                emailSuccessElement.innerHTML = '<img src="' + jfbcRoot + 'images/cancel_f2.png" width="20" height="20">' + jfbcEmailIsInUse;
            }
        },

        isEmail: function(text)
        {
            var pattern = "^[\\w-_\.]*[\\w-_\.]\@[\\w]\.+[\\w]+[\\w]$";
            var regex = new RegExp(pattern);
            return regex.test(text);
        }
    },

    checkPermission: function(permission, callback)
    {
        FB.ensureInit(function()
        {
            FB.Connect.requireSession(function()
            {
                FB.Connect.showPermissionDialog(permission,
                    function(result)
                    {
                        callback();
                    }, false, null);
            });
        });

        return false;
    },

    social: {
        comment: {
            create: function(response)
            {
                var url = 'option=com_jfbconnect&controller=social&task=commentCreate&href=' + encodeURIComponent(escape(response.href)) + '&commentID=' + response.commentID;
                jfbc.ajax(url);
            }
        },
        like: {
            create: function(response)
            {
                var url = 'option=com_jfbconnect&controller=social&task=likeCreate&href=' + encodeURIComponent(escape(response));
                jfbc.ajax(url);
            }
        }
    },

    canvas: {
        checkFrame: function()
        {
            if (top == window)
            { // crude check for any frame
                if (window.location.search == "")
                    top.location.href = window.location.href + '?jfbcCanvasBreakout=1';
                else
                    top.location.href = window.location.href + '&jfbcCanvasBreakout=1';
            }
        }
    },

    ajax: function(url)
    {
        var mooVer = MooTools.version.split(".");
        if (mooVer[1] == '2' || mooVer[1] == '3') // Joomla 1.5 w/mtupgrade or J1.6
        {
            var req = new Request({
                method: 'get',
                url: jfbcBase + 'index.php?' + url
            }).send();
        }
        else
        {
            var myXHR = new XHR({
                method:'get'
            }).send('index.php', url);
        }
    }
}