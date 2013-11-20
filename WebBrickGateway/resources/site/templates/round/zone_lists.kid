<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
#Some ideas being though about. Please leave for now.
#
# In an ideal world these tables will come from a configuration file
#
    # these are the possible zones on the left
    zonelist = [
        "hotwater",
        "kitchen",
        "dining",
        "sittingroom",
        "office",
        "playroom",
        "masterbed",
        "ensuite",
        "kidsrooms",
        "guestbed",
        "gndbath",
        "upbath",
        "hall",
        "landing",
        "outside",
        "gardenroom",
        "garage",
        "cameras",
        "gate",
        "notused",
        "allzones",
        ]
    # This needs all the above and the first 3...
    validity = {
        "": ['audio','lighting','video','security','heating','general','ventilation'],
        "general": ['audio','lighting','video','security','heating','general','ventilation'],
        "overview": ['audio','lighting','video','security','heating','general','ventilation'],
        "hotwater": ['heating',],
        "dining": ['audio','lighting','heating','general'],
        "office": ['lighting','heating','general'],
        "hall": ['lighting','heating'],
        "sittingroom": ['audio','lighting','video','heating','general'],
        "gardenroom": ['lighting','heating'],
        "upbath": ['lighting','heating'],
        "ensuite": ['lighting','heating'],
        "gndbath": ['lighting','heating'],
        "playroom": ['lighting','heating','general'],
        "kitchen": ['audio','lighting','heating','general'],
        "masterbed": ['audio','lighting','heating','general'],
        "landing": ['lighting','heating'],
        "guestbed": ['lighting','heating'],
        "notused": ['heating'],
        "kidsrooms": ['audio','lighting','heating','general'],
        "outside": ['lighting','general'],
        "garage": ['lighting'],
        "cameras": ['security'],
        "gate": ['security'],
        "allzones": ['general'],
        }

    # key, title, icon
    functionaldetails = {
        'audio': ("Audio","funciconaudio.png"),
        'lighting': ("Lighting","funciconlighting.png"),
        'video': ("Video","funciconvideo.png"),
        'security': ("Security","funciconsecurity.png"),
        'heating': ("Heating","funciconheating.png"),
        'ventilation': ("Ventilation","funciconventilation.png"),
        }
        
    # key, title, icon
    zonedetails = {
        "general": ("","zoneiconlivingroom.png"),
        "hotwater": ("Hot Water","zoneiconlivingroom.png"),
        "dining": ("Dining","zoneiconlivingroom.png"),
        "office": ("Office","zoneiconlivingroom.png"),
        "hall": ("Hall","zoneiconlivingroom.png"),
        "sittingroom": ("Sitting Room","zoneiconlivingroom.png"),
        "gardenroom": ("Garden room","zoneiconlivingroom.png"),
        "upbath": ("Up Bath","zoneiconlivingroom.png"),
        "ensuite": ("Ensuite","zoneiconlivingroom.png"),
        "gndbath": ("Gnd Bath","zoneiconlivingroom.png"),
        "playroom": ("Play Room","zoneiconlivingroom.png"),
        "kitchen": ("Kitchen","zoneiconkitchen.png"),
        "masterbed": ("Master Bed","zoneiconbedroom.png"),
        "landing": ("Landing","zoneiconlivingroom.png"),
        "guestbed": ("Guest Bed","zoneiconbedroom.png"),
        "notused": ("Not Used","zoneiconlivingroom.png"),
        "kidsrooms": ("Kids Rooms","zoneiconbedroom.png"),
        "outside": ("Outside","zoneiconlivingroom.png"),
        "garage": ("Garage","zoneiconlivingroom.png"),
        "cameras": ("Cameras","zoneiconlivingroom.png"),
        "gate": ("Gate","zoneiconlivingroom.png"),
        "allzones": ("More Zones","zoneiconlivingroom.png"),
        }
        
    def make_page_link( zn, fnc, pg):
        if zn:
            return "%s_%s_%s" % (zn, fnc, pg)
        return "%s_%s" % (fnc, pg)
?>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" xmlns:wb="http://id.webbrick.co.uk/" >

    <ul py:def="output_zone_links( cur_zone_str, cur_func_str)" class="divider29px">
        <li py:for="k in zonelist" py:if="cur_func_str in validity[k]">
            <wb:simpleLinkList target="/template/${k}_${cur_func_str}_overview" iconimage="zoneicons/${zonedetails[k][1]}">
                <span py:if="cur_zone_str == k" class="selected">${zonedetails[k][0]}</span>
                <span py:if="cur_zone_str &lt;&gt; k" py:strip="True">${zonedetails[k][0]}</span>
            </wb:simpleLinkList>
        </li>
    </ul>
    
    <!-- ! This can be done in a better way by modifying output_zone_links, but since it works no tempering atm.
        The below function will display all zones independant of their validity, this allows to display all zones easily.
        Future Improvement: 
            Previous function to include third parameter to define validity seprate from cur_func_str
            (Reminder: Can py:def be overloaded?)
            --> 
    <ul py:def="output_zone_links_all( cur_zone_str, cur_func_str)" class="divider29px">
        <li py:for="k in zonelist" py:if="k &lt;&gt; 'allzones'">
            <wb:simpleLinkList target="/template/${k}_${cur_func_str}_overview" iconimage="zoneicons/${zonedetails[k][1]}">
                <span py:if="cur_zone_str == k" class="selected">${zonedetails[k][0]}</span>
                <span py:if="cur_zone_str &lt;&gt; k" py:strip="True">${zonedetails[k][0]}</span>
            </wb:simpleLinkList>
        </li>
    </ul>

    <span py:def="output_functional_links( cur_zone_str, cur_func_str,  valid_flags )" py:strip="True">
        <wb:simpleLinkLarge 
                target="/media" 
                id="funcitemaudio" 
                iconimage="funcicons/funciconaudio.png" 
                py:if="'audio' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'audio'" class="selected">Audio</span>
            <span py:if="cur_func_str &lt;&gt; 'audio'" py:strip="True">Audio</span>
        </wb:simpleLinkLarge>
        <wb:simpleLinkLarge 
                target='/template/${make_page_link(cur_zone_str,"lighting","overview")}' 
                id="funcitemlighting" 
                iconimage="funcicons/funciconlighting.png" 
                py:if="'lighting' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'lighting'" class="selected">Lighting</span>
            <span py:if="cur_func_str &lt;&gt; 'lighting'" py:strip="True">Lighting</span>
        </wb:simpleLinkLarge>
        <wb:simpleLinkLarge 
                target='/template/${make_page_link(cur_zone_str,"video","overview")}' 
                id="funcitemvideo" 
                iconimage="funcicons/funciconvideo.png" 
                py:if="'video' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'video'" class="selected">Video</span>
            <span py:if="cur_func_str &lt;&gt; 'video'" py:strip="True">Video</span>
        </wb:simpleLinkLarge>
        <wb:simpleLinkLarge 
                target='/template/${make_page_link(cur_zone_str,"security","overview")}' 
                id="funcitemsecurity" 
                iconimage="funcicons/funciconsecurity.png" 
                py:if="'security' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'security'" class="selected">Security</span>
            <span py:if="cur_func_str &lt;&gt; 'security'" py:strip="True">Security</span>
        </wb:simpleLinkLarge>
        <wb:simpleLinkLarge 
                target='/template/${make_page_link(cur_zone_str,"heating","overview")}' 
                id="funcitemheating" 
                iconimage="funcicons/funciconheating.png" 
                py:if="'heating' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'heating'" class="selected">Heating</span>
            <span py:if="cur_func_str &lt;&gt; 'heating'">Heating</span>
        </wb:simpleLinkLarge>
        <wb:simpleLinkLarge 
                target='/template/${make_page_link(cur_zone_str,"ventilation","overview")}' 
                id="funcitemventilation" 
                iconimage="funcicons/funciconventilation.png" 
                py:if="'ventilation' in validity[cur_zone_str]">
            <span py:if="cur_func_str == 'ventilation'" class="selected">Ventilation</span>
            <span py:if="cur_func_str &lt;&gt; 'ventilation'">Ventilation</span>
        </wb:simpleLinkLarge>
    </span>
</html>
