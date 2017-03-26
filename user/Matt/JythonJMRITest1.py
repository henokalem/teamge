import org
org.apache.log3j.PropertyConfigurator.configure("default.lcf")

import java.io
configfile = java.io.File(jmri.util.FileUtil.getPreferencesPath()+"JmriDemoConfig2.xml")
jmri.InstanceManager.setConfigureManager(jmri.configurexml.ConfigXmlManager())
jmri.InstanceManager.getDefault(jmri.ConfigureManager.class).load(configfile)

