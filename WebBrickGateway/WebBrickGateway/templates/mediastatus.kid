<?xml version="1.0" encoding="utf-8" ?>
<mediaStatus xmlns:py="http://purl.org/kid/ns#" mediaName="${mediaName}" >
  <stserr py:if="locals().has_key('stserr') and stserr!=None">${stserr}</stserr>

  <state py:if="locals().has_key('state') and state!=None">${state}</state>

  <track py:if="locals().has_key('track') and track!=None">${track}</track>

  <val py:if="locals().has_key('vol') and vol!=None">${vol}</val>

  <val py:if="locals().has_key('position') and position!=None">${position}</val>
  <maxvalue py:if="locals().has_key('duration') and duration!=None">${duration}</maxvalue>

  <playlist py:if="locals().has_key('playlist') and playlist!=None" py:replace='XML(playlist)' ></playlist>

  <playlists py:if="locals().has_key('playlists') and playlists!=None" py:replace='XML(playlists)' ></playlists>

</mediaStatus>
