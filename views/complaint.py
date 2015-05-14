# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from inviMarket.models import Trade, Complaint, Email
from inviMarket.forms import CommentsForm
from django.conf import settings
from django.utils.translation import ugettext as _
import mailbox

def complaint(request, trade_id):
    """
    Store an user complaint in :model:`inviMarket.Complaint`, related to
    :model:`inviMarket.Trade` and :model:`auth.User`.

    **Context**

    ``form``
      An instance of the complaint form.

    ``trade``
      An instance of the trade the user is complaining about.

    ``error``
      A string variable informing about any error.

    **Template:**

    :template:`inviMarket/complaint.html`

    """
    error = form = None
    user = request.user
    trade = get_object_or_404(
        Trade.objects.select_related('receptor', 'proposer'), pk=trade_id)
    # Check if the user can make the complaint
    if user != trade.proposer and user != trade.receptor:
        return redirect('index')
    elif Complaint.objects.filter(user=user, trade=trade).exists():
        error = _("You have already submitted a complaint for this trade.")
    elif trade.age() < settings.SENDING_DEADLINE:
        error = _("You have to wait seven days to make a complaint.")
    elif trade.age() > settings.COMPLAINT_DEADLINE:
        error = _("The complaint period has expired.")
    elif request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            complaint = Trade(user=user, trade=trade, comments=comments)
            complaint.save()
            # Store a copy of the emails received by the user in the database
            dirname = settings.MAILDIR + user.username
            mbox = mailbox.Maildir(dirname, factory=None, create=None)
            for message in mbox:
                for part in message.walk():
                    if part.get_content_type() == 'text/plain':
                        text = part.get_payload()
                        break
                    elif part.get_content_type() == 'text/html':
                        text = part.get_payload()
                        break
                email = Email(complaint=complaint, from_address=message['from'],
                              subject=message['subject'], text=text)
                email.save()
            return redirect('complaint_submited')
    else:
        form = CommentsForm()
    return render(request, 'complaint.html', {
        'form': form,
        'trade': trade,
        'error': error,
        })