#
#    Never change this to a DOS file or you'll get a '?' in your file names
#    Andy May 2008
#
# REM generate 16 zones
cp -f templates/zonetemplate.xml "zone1.xml"
sed -e "s:zonetemplate:zone1:" -i zone1.xml
cp -f templates/zonetemplate.xml "zone2.xml"
sed -e "s:zonetemplate:zone2:" -i zone2.xml
cp -f templates/zonetemplate.xml "zone3.xml"
sed -e "s:zonetemplate:zone3:" -i zone3.xml
cp -f templates/zonetemplate.xml "zone4.xml"
sed -e "s:zonetemplate:zone4:" -i zone4.xml
cp -f templates/zonetemplate.xml "zone5.xml"
sed -e "s:zonetemplate:zone5:" -i zone5.xml
cp -f templates/zonetemplate.xml "zone6.xml"
sed -e "s:zonetemplate:zone6:" -i zone6.xml
cp -f templates/zonetemplate.xml "zone7.xml"
sed -e "s:zonetemplate:zone7:" -i zone7.xml
cp -f templates/zonetemplate.xml "zone8.xml"
sed -e "s:zonetemplate:zone8:" -i zone8.xml
cp -f templates/zonetemplate.xml "zone9.xml"
sed -e "s:zonetemplate:zone9:" -i zone9.xml
cp -f templates/zonetemplate.xml "zone10.xml"
sed -e "s:zonetemplate:zone10:" -i zone10.xml
cp -f templates/zonetemplate.xml "zone11.xml"
sed -e "s:zonetemplate:zone11:" -i zone11.xml
cp -f templates/zonetemplate.xml "zone12.xml"
sed -e "s:zonetemplate:zone12:" -i zone12.xml
cp -f templates/zonetemplate.xml "zone13.xml"
sed -e "s:zonetemplate:zone13:" -i zone13.xml
cp -f templates/zonetemplate.xml "zone14.xml"
sed -e "s:zonetemplate:zone14:" -i zone14.xml
cp -f templates/zonetemplate.xml "zone15.xml"
sed -e "s:zonetemplate:zone15:" -i zone15.xml
cp -f templates/zonetemplate.xml "zone16.xml"
sed -e "s:zonetemplate:zone16:" -i zone16.xml
# REM genarete 6 zone groups
cp -f templates/zonegrouptemplate.xml "zonegroup1.xml"
sed -e "s:zonegrouptemplate:1:" -i zonegroup1.xml
cp -f templates/zonegrouptemplate.xml "zonegroup2.xml"
sed -e "s:zonegrouptemplate:2:" -i zonegroup2.xml
cp -f templates/zonegrouptemplate.xml "zonegroup3.xml"
sed -e "s:zonegrouptemplate:3:" -i zonegroup3.xml
cp -f templates/zonegrouptemplate.xml "zonegroup4.xml"
sed -e "s:zonegrouptemplate:4:" -i zonegroup4.xml
cp -f templates/zonegrouptemplate.xml "zonegroup5.xml"
sed -e "s:zonegrouptemplate:5:" -i zonegroup5.xml
cp -f templates/zonegrouptemplate.xml "zonegroup6.xml"
sed -e "s:zonegrouptemplate:6:" -i zonegroup6.xml
# Done
