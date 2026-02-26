# Import student data

library(readtext)

file_path <- "C:\\Users\\mwl04747\\Box\\1. Teaching\\EA030\\Activities\\05_EJnPi -- Github\\Student_Data_2025\\PiZ2_ea30_sp25_v1.log"

ZX.log = readtext(file_path)

head(ZX.log)

processFile = function(filepath) {
  con = file(filepath, "r")
  while ( TRUE ) {
    line = readLines(con, n = 1)
    if ( length(line) == 0 ) {
      break
    }
    print(line)
  }
  
  close(con)
}

z.log = processFile(file_path); z.log

z.log



z.log = readLines(file_path); z.log

gsub("^\\S+ ", "", z.log) # removes everything before first space
sub(".* ", "", z.log) # selects everything after last space



z = data.frame(Date = substring(z.log, 1, 10), Time = substring(z.log, 12, 21),
               param = substring(z.log, 31, 35), value = substring(z.log, 36, 45)); z

z$value


# Returns string without leading white space
trim.leading <- function (x)  sub("^\\s+", "", x)

z$value2 = trim.leading(z$value)

z$units = gsub(" [^ ]+$|^.*? ", "", z$value2)
z$value3 = as.numeric(sub(" .*", "", z$value2))

str(z)

startrows = which(z$Date=="RPi ZeroW ")

z$param[startrows-1] <- "START"
z$value3[startrows-1] <- 0

data = z[!is.na(z$value3),]; data

data = subset(data, select = c(Date, Time, param, value3)); data

# format date/time

names(data)= c("Date", "Time", "Param", "Value"); data

write.csv(data, "C:\\Users\\mwl04747\\Box\\1. Teaching\\EA030\\Activities\\05_EJnPi -- Github\\Student_Data_2025\\PiZ2.csv" )

test = read.csv("C:\\Users\\mwl04747\\Box\\1. Teaching\\EA030\\Activities\\05_EJnPi -- Github\\Student_Data_2025\\PiZ2.csv")


str(test)

