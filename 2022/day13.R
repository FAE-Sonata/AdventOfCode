setwd("C:/HY/Python_exploration/advent_of_code/2022")
libraries_needed<-c("jsonlite", "readtext", "stringr", "magrittr")
lapply(libraries_needed,require,character.only=T)
rm(libraries_needed)

get_first<-function(logicals) {
  return(logicals %>% which %>% min)
}

compare_vectors<-function(v1, v2){
  L1<-length(v1); L2<-length(v2); N<-min(L1, L2)
  if(max(L1, L2) == 0) return(0)
  if(N == 0) return(ifelse(L1 == 0, 1, -1))
  if(L1 == L2 && v1 == v2) return(0)
  left_heavy<-sapply(seq(N), function(k) v1[k] > v2[k])
  right_heavy<-sapply(seq(N), function(k) v1[k] < v2[k])
  if(!any(left_heavy) & any(right_heavy)) return(1)
  if(any(left_heavy)) {
    first_right<-ifelse(any(right_heavy), get_first(right_heavy), -1)
    first_left<-get_first(left_heavy)
    return(ifelse(first_right < 0 | first_right > first_left, -1, 1))
  }
  else return(ifelse(L1 < L2, 1, -1))
}

# TODO: fix recursive un-packing (e.g. 8th example in test file)
signal_compare<-function(pairs) {
  stopifnot(length(pairs) %% 2 == 0)
  NUM_PAIRS<-length(pairs) / 2
  pairs_json<-sapply(seq(NUM_PAIRS), FUN=function(k) {
    first<-fromJSON(pairs[2*k-1])
    second<-fromJSON(pairs[2*k])
    L1<-length(first); L2<-length(second)
    if(is.integer(first) & is.integer(second))
      return(compare_vectors(first, second) >= 0)
    idx<-1
    while(idx <= min(L1, L2)) {
      trav1<-first[idx]; trav2<-second[idx]
      while(!(is.integer(trav1) & is.integer(trav2))) {
        if(is.list(trav1) & is.list(trav2))  {
          while(is.list(trav1) & is.list(trav2))  {
            trav1<-trav1[[1]]; trav2<-trav2[[1]]
            if(length(trav1) == 0) return(T) # trav1<-integer()
            if(length(trav2) == 0) return(F) # trav2<-integer()
          }
        }
        else {
          is_list1<-is.list(trav1); is_list2<-is.list(trav2)
          stopifnot(xor(is_list1, is_list2))
          if(is_list1) trav2<-list(trav2)
          else trav1<-list(trav1)
        }
      }
      if(is.integer(trav1) & is.integer(trav2)) {
        outcome_comparator<-compare_vectors(trav1, trav2)
        if(outcome_comparator != 0) return(outcome_comparator > 0)
      }
      idx<-idx + 1
    }
    return(ifelse(L1 == L2, T, L1 < L2))
  })
  return(which(pairs_json))
}

process<-function(fn) {
  pairs_raw<-readtext(fn)
  pairs_lines<-str_split(pairs_raw$text, "\\n")[[1]] %>%
    Filter(f=function(s) nchar(s) > 0)
  return(signal_compare(pairs_lines))
}
# signals<-fromJSON("files/day13.txt")

print(process("files/day13-test.txt"))