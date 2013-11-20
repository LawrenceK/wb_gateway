REM generate 16 zones
copy templates\zonetemplate.xml zone1.xml
sed -e "s:zonetemplate:zone1:" -i zone1.xml
copy templates\zonetemplate.xml zone2.xml
sed -e "s:zonetemplate:zone2:" -i zone2.xml
copy templates\zonetemplate.xml zone3.xml
sed -e "s:zonetemplate:zone3:" -i zone3.xml
copy templates\zonetemplate.xml zone4.xml
sed -e "s:zonetemplate:zone4:" -i zone4.xml
copy templates\zonetemplate.xml zone5.xml
sed -e "s:zonetemplate:zone5:" -i zone5.xml
copy templates\zonetemplate.xml zone6.xml
sed -e "s:zonetemplate:zone6:" -i zone6.xml
copy templates\zonetemplate.xml zone7.xml
sed -e "s:zonetemplate:zone7:" -i zone7.xml
copy templates\zonetemplate.xml zone8.xml
sed -e "s:zonetemplate:zone8:" -i zone8.xml
copy templates\zonetemplate.xml zone9.xml
sed -e "s:zonetemplate:zone9:" -i zone9.xml
copy templates\zonetemplate.xml zone10.xml
sed -e "s:zonetemplate:zone10:" -i zone10.xml
copy templates\zonetemplate.xml zone11.xml
sed -e "s:zonetemplate:zone11:" -i zone11.xml
copy templates\zonetemplate.xml zone12.xml
sed -e "s:zonetemplate:zone12:" -i zone12.xml
copy templates\zonetemplate.xml zone13.xml
sed -e "s:zonetemplate:zone13:" -i zone13.xml
copy templates\zonetemplate.xml zone14.xml
sed -e "s:zonetemplate:zone14:" -i zone14.xml
copy templates\zonetemplate.xml zone15.xml
sed -e "s:zonetemplate:zone15:" -i zone15.xml
copy templates\zonetemplate.xml zone16.xml
sed -e "s:zonetemplate:zone16:" -i zone16.xml

REM genarete 6 zone groups
copy templates\zonegrouptemplate.xml zonegroup1.xml
sed -e "s:zonegrouptemplate:1:" -i zonegroup1.xml
copy templates\zonegrouptemplate.xml zonegroup2.xml
sed -e "s:zonegrouptemplate:2:" -i zonegroup2.xml
copy templates\zonegrouptemplate.xml zonegroup3.xml
sed -e "s:zonegrouptemplate:3:" -i zonegroup3.xml
copy templates\zonegrouptemplate.xml zonegroup4.xml
sed -e "s:zonegrouptemplate:4:" -i zonegroup4.xml
copy templates\zonegrouptemplate.xml zonegroup5.xml
sed -e "s:zonegrouptemplate:5:" -i zonegroup5.xml
copy templates\zonegrouptemplate.xml zonegroup6.xml
sed -e "s:zonegrouptemplate:6:" -i zonegroup6.xml

REM genarete heatsource 1 - boiler
copy templates\zoneheatsourceboiler.xml zoneheatsource1.xml
sed -e "s:heatsource/boiler:heatsource/1:" -i zoneheatsource1.xml
copy templates\zoneheatsourcegroundsource.xml zoneheatsource2.xml
sed -e "s:heatsource/groundsource:heatsource/2:" -i zoneheatsource2.xml
copy templates\zoneheatsourcesolar.xml zoneheatsource3.xml
sed -e "s:heatsource/solar:heatsource/3:" -i zoneheatsource3.xml
