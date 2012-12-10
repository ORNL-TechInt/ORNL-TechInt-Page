function about()
{
    /* parent.nav.location="projects.html"; */
    clear_frame("nav");
    parent.content.location="about.html";
}

function contact()
{
    clear_frame("nav");
    parent.content.location="contact.html";
}

function jobs()
{
    clear_frame("nav");
    parent.content.location="jobs.html";
}

function members()
{
    parent.nav.location="members.html";
    parent.content.location="vazhkudai.html";
}

function projects()
{
    parent.nav.location="projects.html";
    parent.content.location="storage.html";
}

function publications()
{
    parent.nav.location="pubnav.html";
    parent.content.location="publications.html";
}

function software()
{
    parent.nav.location="swnav.html";
    parent.content.location="software.html";
}

function clear_frame(fid)
{
    var frame = document.getElementById(fid),
    frameDoc = frame.contentDocument || frame.contentWindow.document;
    if (frameDoc.documentElement != null) {
        frameDoc.removeChild(frameDoc.documentElement);
    }
}