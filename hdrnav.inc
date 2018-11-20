  <div class="header">
    <div id="hbanner">
      <table class="header"><tr>
        <td id="logo">
           <a href="https://www.olcf.ornl.gov" target="other">
             <img src="images/olcf-logo.png" alt="OLCF Logo"/>
           </a>
        </td>
        <td id="page_title"><h1>Technology Integration</h1></td>
      </tr></table>
    </div>

    <div class="navbar">
    <ul class="nav">
%ifeq(self.filetype, 'index')
      <li class="current_page">
       <a class="current_page" href="index.html">About</a>
%else
      <li>
       <a href="index.html">About</a>
%endif
%ifeq(self.filetype, 'projects')
      <li class="current_page">
       <a class="current_page" href="projects.html">Thrust Areas</a>
%else
      <li><a href="projects.html">Thrust Areas</a>
%endif
        <ul>
          <li><a href="storage.html">File and Storage Systems</a>
          <li><a href="nvm.html">Non-Volatile Memory</a>
          <li><a href="data.html">Data Management</a>
          <li><a href="networking.html">Networking</a>
          <li><a href="architecture.html">System Architecture and Resilience</a>
        </ul>
%ifeq(self.filetype, 'members')
      <li class="current_page">
       <a class="current_page" href="members.html">Members</a>
%else
      <li><a href="members.html">Members</a>
%endif
        <ul>
          <li><a href="atchley.html">Scott Atchley</a>
          <li><a href="brumgard.html">Chris Brumgard</a>
          <li><a href="disney.html">Adam Disney</a>
          <li><a href="griffith.html">Mitch Griffith</a>
          <li><a href="miller.html">Ross Miller</a>
          <li><a href="mowery.html">Sonya Mowery (group secretary)</a>
          <li><a href="oral.html">Sarp Oral</a>
          <li><a href="shin.html">Woong Shin</a>
          <li><a href="sim.html">Hyogi Sim</a>
          <li><a href="simmons.html">James Simmons</a>
          <li><a href="vazhkudai.html">Sudharshan Vazhkudai (group leader)</a>
          <li><a href="fwang.html">Feiyi Wang</a>
          <li><a href="white.html">Vicky White</a>
          <li><a href="xie.html">Bing Xie</a>
          <li><a href="zimmer.html">Chris Zimmer</a>
        </ul>
%ifeq(self.filetype, 'pub')
      <li class="current_page">
       <a class="current_page" href="publications.html">Publications</a>
%else
      <li><a href="publications.html">Publications</a>
%endif
        <ul>
          <li><a href="publications.html#2018">2018</a>
          <li><a href="publications.html#2017">2017</a>
          <li><a href="publications.html#2016">2016</a>
          <li><a href="publications.html#2015">2015</a>
          <li><a href="publications.html#2014">2014</a>
          <li><a href="publications.html#2013">2013</a>
          <li><a href="publications.html#2012">2012</a>
          <li><a href="publications.html#2011">2011</a>
          <li><a href="publications.html#2010">2010</a>
          <li><a href="publications.html#2009">2009 and earlier</a>
        </ul>
%ifeq(self.filetype, 'software')
      <li class="current_page">
       <a class="current_page" href="software.html">Software</a>
%else
      <li><a href="software.html">Software</a>
%endif
        <ul>
          <li><a href="software.html#2012">2012</a>
          <li><a href="software.html#2011">2011</a>
          <li><a href="software.html#2010">2010 and earlier</a>
        </ul>
%ifeq(self.filetype, 'jobs')
      <li class="current_page">
       <!-- <a class="current_page" href="jobs.html">Jobs</a> -->
       <a class="current_page" href="http://www.olcf.ornl.gov/about/careers/"
          target="other">Jobs</a>
%else
      <li><!-- <a href="jobs.html">Jobs</a> -->
       <a href="http://www.olcf.ornl.gov/about/careers/" target="other">Jobs</a>
%endif
%ifeq(self.filetype, 'contact')
      <li class="current_page">
       <a class="current_page" href="contact.html">Contact</a>
%else
      <li><a href="contact.html">Contact Us</a>
%endif
      <li class="navfill">
    </ul>
    </div>
  </div>
