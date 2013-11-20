echo $1 $2
sed -f $1.sed < curzonestr_heating_overview.kid > ../templates/$2_heating_overview.kid
sed -f $1.sed < curzonestr_heating_config.kid > ../templates/$2_heating_config.kid
sed -f $1.sed < curzonestr_heating_schedule.kid > ../templates/$2_heating_schedule.kid
sed -f $1.sed < curzonestr_general_overview.kid > ../templates/$2_general_overview.kid
sed -f $1.sed < curzonestr_security_overview.kid > ../templates/$2_security_overview.kid
sed -f $1.sed < curzonestr_lighting_overview.kid > ../templates/$2_lighting_overview.kid
sed -f $1.sed < curzonestr_video_overview.kid > ../templates/$2_video_overview.kid
sed -f $1.sed < curzonestr_lighting.xml > ../eventdespatch/$2_lighting.xml
