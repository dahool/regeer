from django.conf import settings
from django.contrib.auth.models import User
#from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop as _
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail
from common.i18n import set_user_language
from teams.models import Team
from files.models import *
#from app.log import logger

class FileUpdateNotification(object):
    
    subject = _("Files changed")
    template = 'updater/new_messages.mail'
    
    def __init__(self, user, logger=None):
        self.notifications = {}
        self.user = user
        self.logger = logger

    def add_notification(self, pofile, add_coord = True):
        try:
            t = Team.objects.get(language=pofile.language,project=pofile.release.project)
        except:
            pass
        else:
            if add_coord:
                userlist = list(t.coordinators.all())
            else:
                userlist = []
            if pofile.assigns.all():
                asg = pofile.assigns.get()
                if asg.translate:
                    userlist.append(asg.translate)
                if asg.review:
                    userlist.append(asg.review)
            for user in userlist:
                cur = []
                if self.notifications.has_key(user.id):
                    cur = self.notifications.get(user.id)
                try:
                    cur.index(pofile)
                except:
                    cur.append(pofile)
                    self.notifications[user.id] = cur    

    def check_notification(self, pofile_new, pofile_old, add_coord = True):
        try:
            new_sum = pofile_new.fuzzy + pofile_new.untrans
            actual_sum = pofile_old.fuzzy + pofile_old.untrans
            
            if new_sum > actual_sum:
                self.add_notification(pofile_new, add_coord)
                pofile_new.log.create(user=self.user, action=LOG_ACTION['ACT_UPDATE'])
                
            if new_sum > 0 and pofile_new.status > 0:
                pofile_new.status = 0
                pofile_new.log.create(user=self.user, action=LOG_ACTION['ST_UNREV'])
                    
            elif new_sum == 0 and pofile_new.status < 2:
                # lets try to guess the status
                if pofile_new.assigns.all():
                    assign = pofile_new.assigns.get()
                    if pofile_new.status == 0:
                        if assign.translate:
                            if POFileLog.objects.filter(
                                                        user=assign.translate,
                                                        pofile=pofile_new,action=LOG_ACTION['ACT_UPLOAD']).count()>0:
                                pofile_new.status = 1
                                pofile_new.log.create(user=self.user, action=LOG_ACTION['ST_TRAN'])
                                if assign.review:
                                    set_user_language(assign.review)
                                    assign.review.message_set.create(message=_("File %s ready for review.") % smart_unicode(pofile_new))
                    elif pofile_new.status == 1:
                        if assign.review:
                            if POFileLog.objects.filter(
                                                        user=assign.review,
                                                        pofile=pofile_new,action=LOG_ACTION['ACT_UPLOAD']).count()>0:
                                pofile_new.status = 2
                                pofile_new.log.create(user=self.user, action=LOG_ACTION['ST_REV'])
        except Exception, e:
            if self.logger: self.logger.error(e)
        
    def process_notifications(self):
        try:
            mlist = []
            prefix = getattr(settings, 'EMAIL_SUBJECT_PREFIX','')
            for id in self.notifications.keys():
                user = User.objects.get(pk=id)
                files = "\n".join(["%s" % smart_unicode(f) for f in self.notifications.get(id)])
                set_user_language(user)
                subject = prefix + self.subject
                message = render_to_string(self.template, {'files': files})
                mlist.append((subject, message, None, [user.email]))
            send_mass_mail(mlist, True)
        except Exception, e:
            if self.logger: self.logger.error(e)
            
class POTFileChangeNotification(FileUpdateNotification):
    
    subject = _("POT files updated")
    template = 'updater/pot_changed.mail'    

    def check_notification(self, pofile, pofile_old, add_coord = True):
        try:
            if pofile.potfile.all():
                potfile = pofile.potfile.get()
                if potfile.total != pofile.total or potfile.updated != pofile.potupdated:
                    if self.logger: self.logger.debug("Need merge (%s)" % pofile.filename) 
                    try:
                        n = POTFileNotification.objects.get(pofile=pofile,
                                                                 potfile=potfile)
                    except POTFileNotification.DoesNotExist:
                        POTFileNotification.objects.create(pofile=pofile,
                                                                 potfile=potfile,
                                                                 last=potfile.updated)
                        self.add_notification(pofile, add_coord)
                    else:
                        if n.last != potfile.updated:
                            n.last = potfile.updated
                            n.save()
                            self.add_notification(pofile, add_coord)
                else:
                    if self.logger: self.logger.debug("File %s is ok" % pofile.filename)
        except Exception, e:
            if self.logger: self.logger.error(e)
                