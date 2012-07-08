supybot-packagist-plugin allows your Supybot users to quickly search http://packagist.org for Composer packages.

Installation
============

Go to **/path/to/supybot/plugins/** and do this:

    $> git clone git://github.com/beryllium/supybot-packagist-plugin.git Packagist

And then add `Packagist` to the supybot.plugins list in the .conf file for your Supybot instance.

Then, update your Supybot configuration to enable the plugin, by adding these lines:

    supybot.plugins.Packagist: True
    supybot.plugins.Packagist.public: True

After restarting your supybot, it should load the Packagist plugin and (@find **_keyword_**) should work in your channels.

(I don't know if the @find command conflicts with any other plugins, so let me know if you encounter issues)

Author
======

Created by Kevin Boyd (aka "Beryllium"), http://beryllium.ca/
