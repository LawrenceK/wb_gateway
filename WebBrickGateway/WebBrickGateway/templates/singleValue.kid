<?xml version="1.0" encoding="utf-8" ?>
<value xmlns:py="http://purl.org/kid/ns#">
  <err py:if="hasattr(self, 'stserr') and stserr">${stserr}</err>
  <val py:if="hasattr(self, 'stsval')">${stsval}</val>
</value>
