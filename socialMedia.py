class SocialMedia:
    # def __init__(self):
    #     pass
    
    def GetSocialMediaSites_NiceNames(self):
        return {
            'facebook':'FaceBook',
            'gmail':'GMail',
            'twitter':'Twitter',
            'whatsapp':'WhatsApp',
        }

    def GetSocialMediaSites_WithShareLinks_OrderedByPopularity(self):
        return [
            'facebook',
            'whatsapp',
            'twitter',
            'linkedin',
            'gmail',
            'copy'
        ]
    
    def GetSocialMediaSites_WithShareLinks_OrderedByAlphabet(self):
        socialmediasites = self.GetSocialMediaSites_NiceNames().keys()
        socialmediasites.sort()
        return socialmediasites
    
    def GetSocialMediaSiteLinks_WithShareLinks(self, args):
        safeargs = [
            'url',
            'title',
            'image',
            'desc',
            'appid',
            'redirecturl',
            'via',
            'hash_tags',
            'provider',
            'language',
            'user_id',
            'category',
            'phone_number',
            'email_address',
            'cc_email_address',
            'bcc_email_address',
        ]
        
        for safearg in safeargs:
            if not args.get(safearg):
                args[safearg] = ''
        
        text = args['title']
        
        if len(args['desc']):
            text += '%20%3A%20' + args['desc']

        return {
            'facebook':'http://www.facebook.com/sharer.php?u=' + args['url'],
            'gmail':'https://mail.google.com/mail/?view=cm&to=' + args['email_address'] + '&su=' + args['title'] + '&body=' +text+ args['url'] ,
            'linkedin':'https://www.linkedin.com/sharing/share-offsite/?url='+args['url'],
            'twitter':'https://twitter.com/intent/tweet?url=' + args['url'] + '&text=' + text + '&via=' + args['via'] + '&hashtags=' + args['hash_tags'],
            'whatsapp':'https://api.whatsapp.com/send?text=' + text + '%20' + args['url'],
        }

# sm = SocialMedia()
# #socialmediasites = sm.GetSocialMediaSites_WithShareLinks_OrderedByAlphabet()
# socialmediasites = sm.GetSocialMediaSites_WithShareLinks_OrderedByPopularity()
# socialmediaurls = sm.GetSocialMediaSiteLinks_WithShareLinks({
#     'url':'http://www.earthfluent.com/',
#     'title':'EarthFluent',
#     'email_address':'sivaaruna10@gmail.com'
# })
# #print(socialmediaurls.keys())

# for socialmediasite in socialmediasites:
#     print(socialmediasite + " : " + socialmediaurls[socialmediasite])
#     pass