parser grammar MycampusParser;

options {
  tokenVocab=MycampusLexer;
}

@header {
	package myc;
	import org.antlr.runtime.RecognitionException;
	import java.util.Vector;
}

@members {
	Section section = null;
	Schedule schedule = null;
	public SectionHandler handler;
	public boolean debug = false;
	void p(String message) {
	  if(this.debug) {
	    System.out.println("DEBUG:" + message);
	  }
	}
	@Override
	public void reportError(RecognitionException e) {
	  System.err.println("Unexpected token: " 
                     + tokenNames[e.getUnexpectedType()]);
	  System.err.println("@ line: " + e.line);
	  System.err.println("token: '" + e.token.getText() + "'");
	  System.exit(0);
	}
}

start
  : section+ EOF
  ;
  
section
  : title {p("title");}
    term  {p("term");}
    registration  {p("registration");}
    levels  {p("levels");}
    (instructors
    {
      p("instructors");
      this.section.instructor_list.addAll($instructors.list);
    }
    )?
    campus {p("campus");}
    credits?
    availability {p("availability");}
    (schedule {p("schedule");})*
    (comments)? 
    {
    this.handler.process(this.section);
    }
  ;
  
title
  : START_TITLE
    TEXT
    END_BR
    {
      this.section = new Section();
      this.section.title = $TEXT.text;
      p("section.title=" + this.section.title);
    }
  ;

term
  : START_TERM TEXT END_BR 
    {
      this.section.semester = $TEXT.text;
    }
  ;

registration
  : START_REGISTRATION TEXT END_BR
    {
      this.section.registration = $TEXT.text;
    }
  ;

levels
  : START_LEVELS TEXT END_BR
    {
      this.section.levels = $TEXT.text;
    }
  ;

instructors returns [List<Instructor> list]
  : START_INSTRUCTORS
    instructor_list
    END_INSTRUCTORS
    {
      $list = $instructor_list.list;
    }
  ;
  
fragment instructor_list returns [List<Instructor> list]
  : 
  {
    $list = new Vector<Instructor>();
    p("\t\tinstructor_list");
  }
  ( n=TEXT
    { // Split by ',' and add to instructor
      for(String name: $n.text.split("\\s*,\\s*"))
        if(name.trim().length() > 0) {
          list.add(new Instructor(name.trim()));
          p("adding instructor \"" + name.trim() + "\"");
        }
    }
  | START_INSTRUCTOR_TITLE t=TEXT END_INSTRUCTOR_TITLE
    { // Modify the last instructor title
      if(list.size() > 0) {
        Instructor person = list.get(list.size()-1);
        person.position = $t.text.trim();
        p("\"" + person.name + "\" has position \"" + person.position + "\"");
      }
    }
  | TBA
  )+
  ;

campus
  : START_BOLD
    UOD?
    x=TEXT
    END_BOLD
    START_BOLD
    TEXT
    END_BOLD
    {
      this.section.campus = $x.text;
    }
  ;

credits
  : START_LECTURE_SCHEDULE_TYPE
    TEXT 
    END_BR
    {
      this.section.credits = $TEXT.text;
    }
  ;

availability
  : START_AVAILABILITY
    ( START_AVAILABILITY_VALUE 
      TEXT
      {
        /* 
         * Availability is the row consisting of (Capacity / Actual / Remaining)
         */ 
        this.section.availability.add($TEXT.text);
      }
      END_AVAILABILITY_VALUE
    )+
    END_AVAILABILITY
    {
      this.section.capacity = this.section.availability.get(0);
      this.section.actual = this.section.availability.get(1);
    }
  ;

schedule
  : START_SCHEDULE
    {
      this.schedule = new Schedule();
      p("\tstart schedule");
    } 
    TEXT? // Week
    type=schedule_entry // Type
    {
      this.schedule.type = $type.text;
      p("schedule.type = " + this.schedule.type);
    }
    time=schedule_entry // Time
    {
      this.schedule.time = $time.text;
      p("schedule.time = " + this.schedule.time);
    }
    days=schedule_entry // Days
    {
      this.schedule.days = $days.text;
      p("schedule.days = " + this.schedule.days);
    }
    where=schedule_entry // Where
    {
      this.schedule.where = $where.text;
      p("schedule.where = " + this.schedule.where);
    }
    date=schedule_entry // Date range
    {
      this.schedule.daterange = $date.text;
    }
    schtype=schedule_entry // Schedule type
    {
      this.schedule.scheduletype = $schtype.text;
    } 
    START_SCHEDULE_VALUE {p("\tstart_schedule_value");}
    instructor_list
    {
      this.schedule.instructor_list.addAll($instructor_list.list);
    } 
    END_SCHEDULE_VALUE // instructors
    END_SCHEDULE
    {
      this.section.schedule_list.add(this.schedule);
      this.schedule = null; 
    }
  ;
  
fragment schedule_entry returns [String text]
  : START_SCHEDULE_VALUE 
    (
      TBA   {$text = "TBA";}
    | TEXT  {$text = $TEXT.text; p("schedule_entry TEXT=" + $TEXT.text);}
    ) END_SCHEDULE_VALUE
  ;

comments
  : 
  ( START_COMMENTS
    TEXT
    END_COMMENTS
  )+
  ;
